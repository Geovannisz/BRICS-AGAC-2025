from playwright.sync_api import sync_playwright

def verify_schedule():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000/programme/index.html")

        # Verify Thursday changes
        page.get_by_role("button", name="Thursday (11/12)").click()
        # Wait for tab transition
        page.wait_for_timeout(1000)

        # Check for Filipe Abdalla at 08:30
        assert "Filipe Abdalla" in page.inner_text("text=08:30 - 09:30") or "Filipe Abdalla" in page.locator("tr:has-text('08:30 - 09:30')").inner_text()

        # Check for Anzhong Wang and Bin Wang split
        assert "Anzhong Wang" in page.locator("tr:has-text('10:45 - 11:10')").inner_text()
        assert "Bin Wang" in page.locator("tr:has-text('11:10 - 11:35')").inner_text()

        # Check for Poster Session asterisk
        assert "Poster Session*" in page.locator("tr:has-text('17:30 - 18:30')").inner_text()

        # Take screenshot of Thursday
        page.screenshot(path="jules-scratch/thursday_verification.png", full_page=False)

        # Verify Friday changes
        page.get_by_role("button", name="Friday (12/12)").click()
        page.wait_for_timeout(1000)

        # Check absence of 11:10 row or absence of Filipe Abdalla at that time
        # We can check that the row for 11:10 - 12:00 doesn't exist or is different.
        # But actually we removed it.
        # So we can check that "Filipe Abdalla" is NOT in Friday tab?
        # Or just take screenshot.

        page.screenshot(path="jules-scratch/friday_verification.png", full_page=False)

        browser.close()

if __name__ == "__main__":
    verify_schedule()
