#!/usr/bin/env python3
"""Build the Customer Journey Game product page with the shared site layout."""
from pathlib import Path

from build_keynotes import page, write


if __name__ == "__main__":
    body = Path(__file__).with_name("customer_journey_game.html").read_text(encoding="utf-8")
    write(
        "customer-journey-game/index.html",
        page(
            "The Customer Journey Game | CX Institute SA",
            "Explore the Customer Journey Game simulation, six industry editions, and facilitated sessions for teams.",
            "/customer-journey-game/",
            body,
            og_image="/assets/img/game-table.jpg",
            enquiry_href="/#enquire",
        ),
    )
