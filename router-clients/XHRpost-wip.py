from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

ROUTER_URL = "https://192.168.1.64"
PASSWORD = "YOUR_PASSWORD_HERE"

TARGET_TEXT = "get_mesh_device_list_all"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
        )

        context = browser.new_context(
            ignore_https_errors=True,
        )

        page = context.new_page()

        def log_request(request) -> None:
            if TARGET_TEXT not in request.url:
                return

            print("\n=== MATCHING REQUEST ===")
            print("Method:", request.method)
            print("URL:", request.url)
            print("Resource type:", request.resource_type)
            print("Content-Type:", request.headers.get("content-type"))
            print("POST body:", request.post_data)

        def log_response(response) -> None:
            if TARGET_TEXT not in response.url:
                return

            print("\n=== MATCHING RESPONSE ===")
            print("Status:", response.status)
            print("URL:", response.url)
            print("Content-Type:", response.headers.get("content-type"))

            try:
                print("Body:")
                print(response.text())
            except Exception as error:
                print("Could not read response body:", error)

        page.on("request", log_request)
        page.on("response", log_response)

        try:
            page.goto(
                ROUTER_URL,
                wait_until="domcontentloaded",
                timeout=15_000,
            )

            password_field = page.locator(
                'input[type="password"]'
            ).first

            password_field.wait_for(
                state="visible",
                timeout=10_000,
            )

            password_field.fill(PASSWORD)

            login_button = page.locator(
                'button[type="submit"], '
                'input[type="submit"], '
                'button:has-text("Log In"), '
                'button:has-text("Login")'
            ).first

            if login_button.count() > 0:
                login_button.click()
            else:
                password_field.press("Enter")

            client_button = page.locator(
                '[data-cy="networkMapClientBtn"]'
            )

            client_button.wait_for(
                state="visible",
                timeout=20_000,
            )

            client_button.click()

            rows = page.locator(
                ".su-table__row.expandable"
            )

            rows.first.wait_for(
                state="visible",
                timeout=25_000,
            )

            print("\nClient list finished loading.")
            input("Press Enter to close the browser...")

        except PlaywrightTimeoutError as error:
            print("Timed out:", error)

            page.screenshot(
                path="tplink-timeout.png",
                full_page=True,
            )

        finally:
            browser.close()


if __name__ == "__main__":
    main()
