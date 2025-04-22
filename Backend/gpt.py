import os
from playwright.sync_api import sync_playwright
import time
import random
from playwright_stealth import stealth_sync

CRASH_DIR = os.path.join('Backend', 'Crash_Png')

def human_delay(min=0.1, max=1.5):
    """Human-like delay with Gaussian distribution"""
    time.sleep(abs(random.gauss((min + max) / 2, (max - min) / 3)))

def debug_visual(page, element=None):
    """Visual debugging helper"""
    os.makedirs(CRASH_DIR, exist_ok=True)
    timestamp = int(time.time())
    path = os.path.join(CRASH_DIR, f'crash_{timestamp}.png')
    
    if element:
        page.evaluate('''e => {
            e.style.outline = '2px solid red';
            e.style.boxShadow = '0 0 10px rgba(255,0,0,0.5)';
        }''', element)
    
    page.screenshot(path=path)
    return timestamp

def google_search(search_term):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 115)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36'
            ]
        )

        context = browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent=f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 115)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36',
            java_script_enabled=True
        )

        page = context.new_page()
        stealth_sync(page)

        try:
            # Navigate to the chatbot page
            page.goto('https://deepai.org/', timeout=60000)
            human_delay(1, 2)  # Initial page load wait

            # Wait for chat interface to be fully interactive
            page.wait_for_selector('#heroChatBox', state='attached', timeout=20000)
            human_delay(1, 2)

            # Type message with human-like typing simulation
            chat_box = page.query_selector('#heroChatBox')
            for char in search_term:
                chat_box.type(char)
                human_delay(0.05, 0.2)  # Simulate real typing speed
            human_delay(0.5, 1)  # Final pause after typing

            # Click submit button
            submit_button = page.query_selector('#mainSubmitButton')
            submit_button.click()
            
            # Wait for response mechanism (adjust selector as needed)
            try:
                # Wait for either response or 45 seconds timeout
                page.wait_for_selector('.bot-message, .response-container, [data-testid="message"]', 
                                      timeout=45000)
                human_delay(1, 2)  # Additional buffer after detection
            except:
                print("Response timeout reached, proceeding anyway")

            # Capture response (update selector based on actual response elements)
            response_elements = page.query_selector_all('.message-text')
            if response_elements:
                latest_response = response_elements[-1].inner_text()
                response = latest_response.strip()
            else:
                response = "No response detected"

            return response

        except Exception as e:
            timestamp = debug_visual(page)
            return f"Error: {str(e)}\nDebug: {os.path.join(CRASH_DIR, f'crash_{timestamp}.png')}"
        finally:
            human_delay(2, 3)  # Final observation pause
            browser.close()

if __name__ == "__main__":
    result = google_search("Hello, how are you?")
    print("Chat Response:", result)