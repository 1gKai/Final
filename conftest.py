import pytest
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

# Ensure screenshots directory exists
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Logging configuration
log_file = "test_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# WebDriver setup for multiple browsers
@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    browser = request.param
    driver = None


    options = None
    if browser == "chrome":
        options = Options()
        service = ChromeService(r"C:\Users\Acer\Documents\thesis\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        service = FirefoxService(r"C:\Users\Acer\Documents\thesis\geckodriver.exe")
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        service = EdgeService(r"C:\Users\Acer\Documents\thesis\msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=options)

    driver.maximize_window()
    yield driver
    driver.quit()
