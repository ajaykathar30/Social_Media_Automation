from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

# ------------------------------------
# CONFIGURATION
# ------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36")

# ⭐ KEY FIX 1: Eager strategy (Don't wait for ads/images to finish)
options.page_load_strategy = 'eager'

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 10)
driver.set_page_load_timeout(10) # Force stop page load after 10s

# ------------------------------------
# STEP 1 — OPEN GOOGLE TRENDS
# ------------------------------------
print("⚡ Opening Google Trends...")
driver.get("https://trends.google.com/trending?category=9")
time.sleep(2)

try:
    first_trend = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "td.enOdEe-wZVHld-aOtOmf.jvkLtd"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_trend)
    time.sleep(1)
    first_trend.click()
except Exception as e:
    print(f"⚠️ Error clicking trend: {e}")

# ------------------------------------
# STEP 2 — COLLECT URLS
# ------------------------------------
try:
    news_links = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.xZCHj"))
    )
    urls = [a.get_attribute("href") for a in news_links if a.get_attribute("href")]
except:
    print("⚠️ Could not find news links.")
    urls = []

print(f"\nFound {len(urls)} URLs. Starting scrape...")

# ------------------------------------
# STEP 3 — SCRAPE & SAVE
# ------------------------------------
# We open a file to save the results because full text is too long for terminal
with open("scraped_results.txt", "w", encoding="utf-8") as f:
    
    for url in urls:
        print(f"\n⚡ Visiting: {url}")
        
        # --- A. Safe Page Load ---
        try:
            driver.get(url)
        except TimeoutException:
            # ⭐ KEY FIX 2: If it gets stuck, stop loading and scrape what we have
            print("   ⚠️ Timeout (likely ads). Stopping load and scraping anyway...")
            driver.execute_script("window.stop();")
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
            continue
        
        time.sleep(2) # Allow DOM to settle

        # --- B. Headline Extraction ---
        try:
            headline = driver.find_element(By.TAG_NAME, "h1").text
        except:
            headline = driver.title

        # --- C. Smart Content Extraction (The Cascade) ---
        content = ""

        # Strategy 1: Specific Classes for Indian News Sites (TOI, NDTV, etc.)
        if not content:
            try:
                # TOI uses '_s30J', NDTV uses 'story_text', etc.
                body_elem = driver.find_element(By.CSS_SELECTOR, 
                    "div._s30J, div.story_text, div[itemprop='articleBody'], div.content_text, div.art_text"
                )
                content = body_elem.text
            except:
                pass

        # Strategy 2: Semantic <article> tag (Modern standard)
        if not content:
            try:
                content = driver.find_element(By.TAG_NAME, "article").text
            except:
                pass

        # Strategy 3: Fallback to all <p> tags (The "Brute Force" method)
        if not content or len(content) < 100:
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                # Filter out short blurbs/links/copyright text
                clean_ps = [p.text for p in paragraphs if len(p.text) > 40]
                content = "\n\n".join(clean_ps)
            except:
                pass

        # Final check
        if not content:
            content = "[No text extracted - Content might be video or deeply protected]"

        # --- D. Print & Save ---
        print(f"   ✅ Headline: {headline[:60]}...")
        print(f"   📄 Extracted {len(content)} characters.")
        
        # Write to file
        f.write(f"URL: {url}\n")
        f.write(f"HEADLINE: {headline}\n")
        f.write("CONTENT:\n")
        f.write(content)
        f.write("\n" + "="*80 + "\n\n")

driver.quit()
print("\n🎉 Done! Full articles saved to 'scraped_results.txt'")