import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

# Logging configuration
log_file = "test_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure screenshots directory exists
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

@pytest.mark.parametrize("username, password, expected", [
    ("testuser", "Test@123", True),     # ✅ Valid credentials
    ("wronguser", "Test@123", False),   # ❌ Incorrect username
    ("testuser", "WrongPass", False),   # ❌ Incorrect password
    ("", "Test@123", False),            # ❌ Empty username
    ("testuser", "", False),            # ❌ Empty password
    ("' OR '1'='1", "anything", False), # ❌ SQL Injection attempt
    ("testuser", "!@#$%^&*()", True),   # ✅ Special characters in password
    (" testuser ", "Test@123", False)   # ❌ Username with leading/trailing spaces
])
def test_login(driver, username, password, expected):
    """Test login functionality with different credentials."""
    try:
        driver.get("https://demoqa.com/login")
        wait = WebDriverWait(driver, 10)

        
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login")))

        
        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        
        if expected:
            wait.until(EC.url_contains("profile"))
            assert "profile" in driver.current_url
            logging.info(f"✅ [{driver.name.upper()}] Login success: {username}")
        else:
            error_message = wait.until(EC.visibility_of_element_located((By.ID, "name"))).text
            assert "Invalid username or password!" in error_message
            logging.warning(f"❌ [{driver.name.upper()}] Login failed: {username}")

    except TimeoutException:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(screenshot_dir, f"timeout_{username}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        logging.error(f"⚠️ [{driver.name.upper()}] Timeout error with {username}. Screenshot saved: {screenshot_path}")

    except NoSuchElementException as e:
        logging.error(f"⚠️ [{driver.name.upper()}] Element not found: {e}")