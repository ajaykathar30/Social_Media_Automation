from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
options.add_argument("window-size=1400,900")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)
driver.set_page_load_timeout(7)      # ⭐ CRITICAL — prevents timeout

# ------------------------------------
# STEP 1 — OPEN GOOGLE TRENDS PAGE
# ------------------------------------
driver.get("https://trends.google.com/trending?category=9")
time.sleep(1)

driver.execute_script("window.scrollBy(0, 300);")

first_trend = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "td.enOdEe-wZVHld-aOtOmf.jvkLtd"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_trend)
time.sleep(0.4)
first_trend.click()
time.sleep(1)

# ------------------------------------
# STEP 2 — COLLECT ALL NEWS LINKS
# ------------------------------------
news_links = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.xZCHj"))
)

urls = [a.get_attribute("href") for a in news_links if a.get_attribute("href")]

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
    except Exception:
        print("❌ Page load stuck — skipping...")
        driver.execute_script("window.stop();")
        continue

    time.sleep(1)

    # HEADLINE
    try:
        headline = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text
    except:
        headline = "Headline not found"

    # ARTICLE PARAGRAPHS
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    content = "\n".join([p.text for p in paragraphs if len(p.text) > 40])

    print("\nHEADLINE:\n", headline)
    print("\nARTICLE TEXT (first 600 chars):\n", content)
    print("\n-----------------------------------------")

driver.quit()
