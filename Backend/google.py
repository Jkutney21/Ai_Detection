from playwright.sync_api import sync_playwright
import time
import random
import sys
import psutil
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

def kill_process_on_port(port):
    """Kill process running on specified port"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        print(f"Killing process {proc.pid} ({proc.name()})")
                        try:
                            proc.terminate()
                            proc.wait(timeout=3)
                        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                            try:
                                proc.kill()
                            except psutil.NoSuchProcess:
                                pass
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Error killing processes: {str(e)}")

def human_delay(min_delay=0.5, max_delay=2.0):
    """Generate human-like delay"""
    time.sleep(random.uniform(min_delay, max_delay))

def google_search(search_term):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                '--start-maximized'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        page = context.new_page()
        
        try:
            human_delay()
            page.goto('https://search.brave.com/', timeout=60000)
            
            # Handle potential CAPTCHA
            if page.query_selector('text="I\'m not a robot"'):
                print("CAPTCHA detected! Solve manually in the browser...")
                page.pause()
                
            # Accept cookies if present
            try:
                page.click('button:has-text("Accept all") >> visible=true', timeout=3000)
                human_delay()
            except Exception:
                pass

            # Enter search term into the search box
            search_box = page.wait_for_selector('textarea[name="q"], input[name="q"]', timeout=10000)
            for char in search_term:
                search_box.type(char, delay=random.randint(50, 150))
                human_delay(0.1, 0.3)
                
            human_delay(1, 2)
            # Instead of pressing Enter, click the AI answer button
            ai_button = page.wait_for_selector('button#submit-llm-button', timeout=10000)
            ai_button.click()
            print("Clicked the AI answer button")
            
            # Wait for the main answer content to load
            try:
                page.wait_for_selector('#chatllm-main-answer-content', timeout=15000)
            except Exception:
                if page.query_selector('text="detected unusual traffic"'):
                    print("Blocked by search engine. Try:")
                    print("1. Use proxies")
                    print("2. Solve CAPTCHA manually")
                    print("3. Wait before retrying")
                    return

            # Optionally click the "More" button if it exists to expand content
            try:
                more_button = page.wait_for_selector('#llm-show-more-button', timeout=5000)
                if more_button:
                    human_delay(1, 1.5)
                    more_button.click()
                    print("Clicked 'More' button to expand content")
                    human_delay(1, 2)  # Wait for content to expand
            except Exception as e:
                # Log and continue if the "More" button is not found
                print("No 'More' button found; continuing without expansion:", str(e))

            # Extract main answer content
            try:
                result_element = page.wait_for_selector('#chatllm-main-answer-content', timeout=10000)
                content = result_element.inner_text()
                with open('./text/google.txt', 'a') as log_file:
                    # Clean the content by removing unwanted digits and words if needed
                    cleaned_content = ' '.join([word for word in content.split() if not word.isdigit() and word != "False"])
                    log_file.write(cleaned_content.strip() + "\n")
            except Exception as e:
                print(f"Content extraction failed: {str(e)}")
                page.screenshot(path='./Crash_Png/content_error.png')

        except Exception as e:
            print(f"General error: {str(e)}")
            page.screenshot(path='./Crash_Png/search_error.png')
            
        finally:
            human_delay(1, 3)
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Searching for:", ' '.join(sys.argv[1:]))
        search_term = ' '.join(sys.argv[1:])
        google_search(search_term)
    else:
        google_search("Question 1 In Neoaj, which of the accurately describe the use of WITH and RETURN clauses in complex queries? A")
