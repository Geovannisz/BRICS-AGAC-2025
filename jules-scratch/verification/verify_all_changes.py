from playwright.sync_api import sync_playwright
import os
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Start a local server
        os.system('python -m http.server 8000 &')
        time.sleep(2) # Add a delay to allow the server to start

        # Verify bingo page
        page.goto('http://localhost:8000/bingo-program/')
        page.screenshot(path='jules-scratch/verification/bingo.png')

        # Verify committees page
        page.goto('http://localhost:8000/committees/')
        page.screenshot(path='jules-scratch/verification/committees.png')

        # Verify attendees page
        page.goto('http://localhost:8000/attendees/')
        page.wait_for_selector('#attendees-tbody tr')
        page.screenshot(path='jules-scratch/verification/attendees.png')

        # Stop the server
        os.system("ps aux | grep '[p]ython -m http.server' | awk '{print $2}' | xargs kill")

        browser.close()

run()
