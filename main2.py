



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

driver.maximize_window()
driver.get("https://trends.google.com/trending?category=9")

# Scroll a bit so the table loads
driver.execute_script("window.scrollBy(0, 300);")
time.sleep(1)

# 1️⃣ CLICK the trending table data (your exact selector)
first_td = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "td.enOdEe-wZVHld-aOtOmf.jvkLtd")
    )
)

# Scroll into view to avoid click interception
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_td)
time.sleep(0.5)

first_td.click()

# 2️⃣ WAIT for sidebar to load
# Sidebar contains the <a class="xZCHj">
time.sleep(1)  # stability (sidebar animates)
news_links = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.xZCHj"))
)

# 3️⃣ Extract actual URLs
final_links = []
for a in news_links:
    href = a.get_attribute("href")
    if href and href.startswith("http"):
        final_links.append(href)

print("\n--- NEWS CHANNEL LINKS FOUND ---\n")
for link in final_links:
    print(link)

driver.quit()
