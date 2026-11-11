import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHandler } from '../src/index.js';

const env = { RESEND_API_KEY: 'k', FROM_EMAIL: 'web@example.com', TO_EMAIL: 'lynn@cx-company.com' };
const good = { interest: 'game', name: 'Thandi Mokoena', email: 'thandi@acme.co.za', company: 'Acme', message: 'We would like a session for 80 people.', elapsed: 9000 };
const req = (body, headers = {}) => new Request('https://site.test/api/enquiry', {
  method: 'POST', headers: { 'content-type': 'application/json', origin: 'https://site.test', ...headers }, body: JSON.stringify(body)
});
function spy(ok = true) {
  const calls = [];
  const send = async (url, init) => { calls.push({ url, body: JSON.parse(init.body), auth: init.headers.Authorization }); return new Response(JSON.stringify({ id: 'x' }), { status: ok ? 200 : 500 }); };
  return { calls, h: createHandler(send) };
}

test('valid enquiry is emailed to Lynn with reply-to set to the visitor', async () => {
  const { calls, h } = spy();
  const r = await h.fetch(req(good), env);
  assert.equal(r.status, 200); assert.deepEqual(await r.json(), { ok: true });
  assert.equal(calls.length, 1);
  const m = calls[0].body;
  assert.equal(calls[0].url, 'https://api.resend.com/emails');
  assert.equal(calls[0].auth, 'Bearer k');
  assert.deepEqual(m.to, ['lynn@cx-company.com']);
  assert.equal(m.reply_to, 'thandi@acme.co.za');
  assert.match(m.subject, /The Customer Journey Game© – Thandi Mokoena, Acme/);
  assert.match(m.text, /80 people/);
});
test('HTML in fields is escaped', async () => {
  const { calls, h } = spy();
  await h.fetch(req({ ...good, message: '<script>alert(1)</script> hello there' }), env);
  assert.ok(!calls[0].body.html.includes('<script>'));
});
test('header injection via name is neutralised', async () => {
  const { calls, h } = spy();
  await h.fetch(req({ ...good, name: 'Bob\r\nBcc: x@y.com' }), env);
  assert.ok(!/[\r\n]/.test(calls[0].body.subject));
});
test('missing fields are reported, nothing sent', async () => {
  const { calls, h } = spy();
  const r = await h.fetch(req({ interest: 'nope', email: 'bad', elapsed: 9000 }), env);
  assert.equal(r.status, 400);
  const j = await r.json();
  assert.deepEqual(j.fields.sort(), ['company', 'email', 'interest', 'message', 'name']);
  assert.equal(calls.length, 0);
});
test('honeypot and too-fast submissions look successful but send nothing', async () => {
  const { calls, h } = spy();
  assert.equal((await h.fetch(req({ ...good, website: 'spam.com' }), env)).status, 200);
  assert.equal((await h.fetch(req({ ...good, elapsed: 500 }), env)).status, 200);
  assert.equal(calls.length, 0);
});
test('other origins are refused', async () => {
  const { calls, h } = spy();
  assert.equal((await h.fetch(req(good, { origin: 'https://evil.test' }), env)).status, 403);
  assert.equal(calls.length, 0);
});
test('not configured gives 503; provider failure gives 502', async () => {
  assert.equal((await spy().h.fetch(req(good), { TO_EMAIL: 'lynn@cx-company.com' })).status, 503);
  assert.equal((await spy(false).h.fetch(req(good), env)).status, 502);
});
test('GET and oversized bodies are refused', async () => {
  const { h } = spy();
  assert.equal((await h.fetch(new Request('https://site.test/api/enquiry'), env)).status, 405);
  assert.equal((await h.fetch(req({ ...good, message: 'x'.repeat(9000) }), env)).status, 413);
});
test('other paths go to static assets', async () => {
  const { h } = spy();
  const r = await h.fetch(new Request('https://site.test/'), { ...env, ASSETS: { fetch: () => new Response('page') } });
  assert.equal(await r.text(), 'page');
});
