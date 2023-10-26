from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def navigate(access_link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get(access_link)

    title = browser.title

    browser.quit()

    return title