from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

def capture_screenshot(url, path):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage") # Essential for containers

    driver = None
    try:
        # 1. Try using the pre-installed system Chrome (Works on Streamlit Cloud via packages.txt)
        driver = webdriver.Chrome(options=options)
    except Exception:
        # 2. Fallback to webdriver-manager (Works on your local PC)
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    
    # Ensure the target directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    driver.save_screenshot(path)
    driver.quit()