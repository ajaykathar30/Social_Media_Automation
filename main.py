from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Start Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

driver.maximize_window()
driver.get("https://trends.google.com/trending?category=9")

# Scroll a little so table becomes visible
driver.execute_script("window.scrollBy(0, 300);")
time.sleep(1)

# CLICK the first trending item (inside table td)
first_trend = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "td.enOdEe-wZVHld-aOtOmf.jvkLtd")
    )
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_trend)
time.sleep(0.4)
first_trend.click()

# WAIT for the sidebar list to appear
time.sleep(1)

# All news article links
news_links = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.xZCHj"))
)

urls = [a.get_attribute("href") for a in news_links if a.get_attribute("href")]
print("\nExtracted news URLs:")
for u in urls:
    print(" -", u)

print("\n------ SCRAPING EACH ARTICLE ------\n")

# Visit each news site and scrape headline + article body
for url in urls:
    print(f"\nVisiting: {url}")
    driver.get(url)

    # Wait for page to load
    time.sleep(2)

    # Extract HEADLINE
    try:
        headline = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text
    except:
        headline = "Headline not found"

    # Extract ARTICLE TEXT
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    content = "\n".join([p.text for p in paragraphs if len(p.text) > 40])  # filter short junk

    print("\nHEADLINE:\n", headline)
    print("\nARTICLE TEXT (first 600 chars):\n", content[:600])
    print("\n-------------------------------------------")

driver.quit()