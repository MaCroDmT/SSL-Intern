from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
import time, traceback

# Setup Firefox
service = Service()  # Will use geckodriver from PATH
driver = webdriver.Firefox(service=service)
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    # --- Login ---
    driver.get("http://182.160.125.188:8080/erp/login.php")
    driver.find_element(By.ID, "txt_userid").send_keys("prottoy")
    driver.find_element(By.ID, "txt_password").send_keys("12345")
    driver.find_element(By.ID, "submit").click()
    print("Logged in.")

    # --- Step 1: Open Merchandising ---
    merch = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Merchandising")))
    merch.click()
    print("Opened Merchandising.")

    # --- Step 2: Expand Sweater Garments submenu ---
    sweater_toggle = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(normalize-space(.), 'Sweater Garments')]")
        )
    )
    driver.execute_script("arguments[0].click();", sweater_toggle)
    print("Expanded Sweater Garments menu.")

    # --- Step 3: Expand Order Tracking submenu ---
    order_toggle = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(normalize-space(.), 'Order Tracking')]")
        )
    )
    driver.execute_script("arguments[0].click();", order_toggle)
    print("Expanded Order Tracking menu.")

    # --- Step 4: Click Pre-Costing [BOM] ---
    pre_costing = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Pre-Costing [BOM]')]"))
    )
    driver.execute_script("arguments[0].click();", pre_costing)
    print("Opened Pre-Costing [BOM].")

    # --- Step 5: Double-click Job No field ---
    job_no = wait.until(EC.element_to_be_clickable((By.ID, "txt_job_no")))
    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick', {bubbles: true}));", job_no)
    print("Double-clicked Job No.")

    # --- NEW CODE TO BE ADDED ---

    # Wait for the popup/modal to appear. This is the crucial missing step.
    # The company dropdown is inside the popup, so we must wait for it to be present.
    wait.until(EC.visibility_of_element_located((By.ID, "cbo_company_mst")))
    print("Popup with company dropdown is now visible.")

    # --- Step 6: Select company from dropdown ---
    company_dropdown = driver.find_element(By.ID, "cbo_company_mst")
    for option in company_dropdown.find_elements(By.TAG_NAME, "option"):
        if "Sonia and Sweaters Ltd." in option.text:
            option.click()
            print("Selected 'Sonia and Sweaters Ltd.'")
            break

    # --- Step 7: Click the 'Show' button ---
    show_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Show']")))
    show_button.click()
    print("Clicked 'Show' button.")

    # The script now waits in the final state for you to continue.
    time.sleep(5)

except Exception as e:
    print("Automation FAILED:", str(e))
    traceback.print_exc()
    ts = int(time.time())
    driver.save_screenshot(f"error_{ts}.png")
    with open(f"page_{ts}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"Saved debug: error_{ts}.png and page_{ts}.html")

finally:
    print("Automation finished.")
    # driver.quit()