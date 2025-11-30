from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# ------------------------------------
# SELENIUM SETUP
# ------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36")

# ⭐ CRITICAL FIX 1: Eager strategy (Don't wait for ads/images)
options.page_load_strategy = 'eager'

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 10)
driver.set_page_load_timeout(10) # 10 seconds is usually safer than 7

# ------------------------------------
# STEP 1 — OPEN GOOGLE TRENDS PAGE
# ------------------------------------
print("⚡ Opening Google Trends...")
driver.get("https://trends.google.com/trending?category=9")
time.sleep(2) 

# Click the first trend
try:
    first_trend = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "td.enOdEe-wZVHld-aOtOmf.jvkLtd"))
    )
    # Scroll slightly to ensure clickability
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_trend)
    time.sleep(1)
    first_trend.click()
except Exception as e:
    print(f"Error clicking trend: {e}")

# ------------------------------------
# STEP 2 — COLLECT ALL NEWS LINKS
# ------------------------------------
try:
    news_links = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.xZCHj"))
    )
    urls = [a.get_attribute("href") for a in news_links if a.get_attribute("href")]
except Exception as e:
    print("Could not find news links.")
    urls = []

print("\nExtracted URLs:")
for u in urls:
    print(" -", u)

print("\n------ SCRAPING EACH ARTICLE ------\n")

# ------------------------------------
# STEP 3 — VISIT EACH NEWS LINK SAFELY
# ------------------------------------
for url in urls:
    print(f"\n⚡ Visiting: {url}")

    try:
        driver.get(url)
    except TimeoutException:
        # ⭐ CRITICAL FIX 2: Handle timeout but DO NOT SKIP
        print("⚠️ Page load timed out (likely ads). Stopping load and scraping anyway...")
        driver.execute_script("window.stop();")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        continue # Only skip if it's a real connection error (not a timeout)

    # Give it a brief moment for the DOM to settle after stopping
    time.sleep(2)

    # HEADLINE
    try:
        # Try H1 first
        headline = driver.find_element(By.TAG_NAME, "h1").text
    except:
        try:
            # Fallback to Title tag if H1 is missing
            headline = driver.title
        except:
            headline = "Headline not found"

    # ARTICLE PARAGRAPHS
    # Using a slightly safer wait here to ensure body exists
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        
        # Filter: Only text > 40 chars to avoid menu items/copyright text
        content_list = [p.text for p in paragraphs if len(p.text) > 40]
        
        # Join top 5 paragraphs to avoid massive walls of text in terminal
        content = "\n".join(content_list[:5]) 
        
        if not content:
            content = "[No meaningful text content found]"
            
    except Exception as e:
        content = f"Error extracting text: {e}"

    print(f"HEADLINE: {headline}")
    print(f"CONTENT PREVIEW: {content}...") # Print first 300 chars
    print("-" * 40)

driver.quit()