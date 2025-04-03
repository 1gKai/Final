import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
import string

# Logging configuration
log_file = "test_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure screenshots directory exists
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Helper function to generate a random string for username/email
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@pytest.mark.parametrize("username, password", [
    (generate_random_string(), "Test@123"),  # Generate random username and use a fixed password
])
def test_logout(driver, username, password):
    """Test logout functionality after a successful login by creating a new account."""
    try:
        # Step 1: Register a new account
        driver.get("https://demoqa.com/login")
        wait = WebDriverWait(driver, 10)

        # Locate and fill the registration form (assuming DemoQA has these fields)
        # Change these locators based on DemoQA's actual registration form
        register_button = driver.find_element(By.ID, "register_button")  # Adjust if necessary
        
        # Assuming there is a register button that takes you to the registration form
        register_button.click()

        # Locate and fill registration form fields
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        register_button = driver.find_element(By.ID, "register")

        username_field.send_keys(username)  # New random username
        email_field.send_keys(f"{username}@demo.com")  # Email based on username
        password_field.send_keys(password)
        register_button.click()

        # Wait for registration to complete and go to the login page
        wait.until(EC.url_contains("login"))

        # Step 2: Login with the newly created account
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login")

        username_field.send_keys(username)  # Use the same username for login
        password_field.send_keys(password)
        login_button.click()

        # Step 3: Verify login was successful
        wait.until(EC.url_contains("profile"))
        assert "profile" in driver.current_url  # Verify that we are redirected to the profile page after login

        logging.info(f"✅ Login successful for {username}")

        # Step 4: Click on Logout
        logout_button = wait.until(EC.element_to_be_clickable((By.ID, "logout")))  # Adjust if necessary
        logout_button.click()

        # Step 5: Verify logout
        wait.until(EC.url_contains("login"))
        assert "login" in driver.current_url  # Ensure we're redirected to the login page after logout

        logging.info(f"✅ Successfully logged out for {username}")

    except Exception as e:
        logging.error(f"⚠️ Error during logout test: {e}")
        # Optionally take a screenshot on error
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(screenshot_dir, f"logout_error_{username}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)