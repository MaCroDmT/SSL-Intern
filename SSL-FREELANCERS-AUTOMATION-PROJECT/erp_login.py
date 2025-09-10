from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import traceback

# ---------- Config ----------
LOGIN_PAGE = "http://182.160.125.188:8080/erp/login.php"
service = Service()  # assumes geckodriver in PATH
driver = webdriver.Firefox(service=service)
wait = WebDriverWait(driver, 20)

# Credentials from environment
username = os.environ.get("ERP_USERNAME")
password = os.environ.get("ERP_PASSWORD")
if not username or not password:
    raise ValueError("Set environment variables ERP_USERNAME and ERP_PASSWORD before running.")

def find_with_fallback(tries):
    """tries: list of (By, value) - returns first clickable element found"""
    for by, val in tries:
        try:
            el = wait.until(EC.element_to_be_clickable((by, val)))
            return el
        except Exception:
            continue
    return None

def login_success_condition(d):
    """Return True if we detect successful login (URL change or dashboard element present)."""
    try:
        if d.current_url and d.current_url.rstrip("/") != LOGIN_PAGE.rstrip("/"):
            return True
        # look for a known dashboard element - adapt if yours is different
        try:
            d.find_element(By.LINK_TEXT, "Merchandising")
            return True
        except Exception:
            pass
        try:
            d.find_element(By.XPATH, "//h1[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'platform')]")
            return True
        except Exception:
            pass
    except Exception:
        pass
    return False

try:
    driver.get(LOGIN_PAGE)
    print("Opened login page:", LOGIN_PAGE)

    # Find username field (fall back through common attributes)
    username_field = find_with_fallback([
        (By.NAME, "txt_userid"),
        (By.ID, "txt_userid"),
        (By.CLASS_NAME, "user_name"),
        (By.CSS_SELECTOR, "input[placeholder='User Name']"),
        (By.CSS_SELECTOR, "input[type='text']")
    ])
    if not username_field:
        raise RuntimeError("Username field not found (tried txt_userid / id / class / placeholder).")
    username_field.clear()
    username_field.send_keys(username)
    print("Username entered.")

    # Find password field
    password_field = find_with_fallback([
        (By.NAME, "txt_password"),
        (By.ID, "txt_password"),
        (By.CLASS_NAME, "password"),
        (By.CSS_SELECTOR, "input[placeholder='Password']"),
        (By.CSS_SELECTOR, "input[type='password']")
    ])
    if not password_field:
        raise RuntimeError("Password field not found (tried txt_password / id / class / placeholder).")
    password_field.clear()
    password_field.send_keys(password)
    print("Password entered.")

    # Find & click the login button (with fallbacks)
    login_btn = find_with_fallback([
        (By.ID, "submit"),
        (By.NAME, "submit"),
        (By.CLASS_NAME, "login"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']")
    ])
    if not login_btn:
        raise RuntimeError("Login button not found.")
    try:
        login_btn.click()
    except Exception:
        # fallback to javascript click if normal click fails
        driver.execute_script("arguments[0].click();", login_btn)
    print("Login button clicked.")

    # Wait for login success: URL change or dashboard element
    wait.until(login_success_condition)
    print("Login seems successful (URL changed or dashboard element detected).")

    # Example: click Merchandising if present
    try:
        merch = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Merchandising")))
        merch.click()
        print("Clicked 'Merchandising'.")
    except Exception:
        print("Merchandising link not found or clickable — continuing.")

except Exception as e:
    print("ERROR during automation:", str(e))
    traceback.print_exc()
    # Save screenshot & partial page source for debugging
    timestamp = int(time.time())
    screenshot = f"error_{timestamp}.png"
    driver.save_screenshot(screenshot)
    print("Saved screenshot:", screenshot)
    try:
        with open(f"page_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source[:20000])  # write first 20k chars to keep file size reasonable
        print("Saved partial page source: page_{}.html".format(timestamp))
    except Exception:
        pass

finally:
    print("Automation finished.")
    # driver.quit()   # uncomment when you are done debugging
