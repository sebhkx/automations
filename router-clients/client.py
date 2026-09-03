import os
import re

from dotenv import load_dotenv
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)
from playwright.sync_api import (
    sync_playwright,
)

load_dotenv()


ROUTER_URL = os.environ["ROUTER_URL"]
PASSWORD = os.environ["PASSWORD"]


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
        )

        context = browser.new_context(
            ignore_https_errors=True,
        )

        page = context.new_page()

        try:
            page.goto(
                ROUTER_URL,
                wait_until="domcontentloaded",
                timeout=15000,
            )

            password_field = page.locator(
                'input[type="password"]'
            ).first

            password_field.wait_for(
                state="visible",
                timeout=10000,
            )

            password_field.fill(PASSWORD)

            login_button = page.locator(
                'button[type="submit"], '
                'input[type="submit"], '
                'button:has-text("Log In"), '
                'button:has-text("Login")'
            ).first

            if login_button.count():
                login_button.click()
            else:
                password_field.press("Enter")

            client_button = page.locator(
                '[data-cy="networkMapClientBtn"]'
            )

            client_button.wait_for(
                state="visible",
                timeout=5000,
            )

            client_button.click()

            rows = page.locator(".su-table__row.expandable")

            rows.first.wait_for(
                state="visible",
                timeout=15000,
            )

            machines = []

            for index in range(rows.count()):
                row = rows.nth(index)

                info_values = [
                    e.inner_text().strip()
                    for e in row.locator(".info-wrapper").all()
                ]

                # Remove MAC addresses
                cleaned = []
                for value in info_values:
                    lines = value.splitlines()

                    lines = [
                        line
                        for line in lines
                        if not re.fullmatch(
                            r"(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}",
                            line.strip(),
                        )
                    ]

                    cleaned.append("\n".join(lines))

                machines.append(cleaned)

            # Sort alphabetically by machine name (first line of first column)
            machines.sort(
                key=lambda machine: machine[0].splitlines()[0].lower()
            )

            print(f"TP-Link router clients: {len(machines)}\n")

            for machine in machines:
                for value in machine:
                    print(value)

                print()      # blank line

        except PlaywrightTimeoutError as e:
            print("Timed out:", e)

        finally:
            browser.close()


if __name__ == "__main__":
    main()