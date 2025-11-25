from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import time
import random
import os

def setup_driver():
    """Sets up the Chrome Webdriver with strict pathing for the correct browser."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    
    # --- CRITICAL FIX FOR VERSION MISMATCH ---
    # We force Selenium to look in the standard 64-bit folder first.
    # The error log showed it was picking up an old version in "Program Files (x86)"
    
    correct_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    if os.path.exists(correct_path):
        print(f"Found modern Chrome at: {correct_path}")
        options.binary_location = correct_path
    else:
        print("Warning: Could not find Chrome in standard 64-bit folder. Relying on system default.")

    # Ignore certificate errors
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    print("Setting up Chrome Driver...")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
        
    except SessionNotCreatedException as e:
        print("\n" + "!"*50)
        print("CRITICAL ERROR: BROWSER VERSION MISMATCH")
        print("!"*50)
        print(f"Details: {e.msg}")
        print("-" * 20)
        print("TROUBLESHOOTING:")
        print("The script is likely still finding the old Chrome version.")
        print("1. Open 'Add or Remove Programs' in Windows.")
        print("2. Search for Google Chrome.")
        print("3. If you see two versions, uninstall the older one.")
        print("!"*50 + "\n")
        raise SystemExit("Script stopped.")
        
    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
        raise SystemExit("Script stopped.")

def type_numbers(driver):
    """Finds the text on screen and types it."""
    try:
        # Wait for the text container to appear
        text_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "screenBasic-lines"))
        )
        
        # Get all the individual characters/numbers
        characters = text_container.find_elements(By.CSS_SELECTOR, ".token_unit")
        
        print(f"Found {len(characters)} characters to type...")

        body = driver.find_element(By.TAG_NAME, 'body')
        
        for char in characters:
            letter = char.text
            
            # Handle spaces explicitly if needed
            if letter == "": 
                letter = " "
                
            body.send_keys(letter)
            
            # Add a tiny, random human-like delay
            time.sleep(random.uniform(0.05, 0.15)) 
            
        print("Typing sequence finished.")
        return True

    except Exception as e:
        print(f"Could not find text to type. (Are you on the score screen?)")
        return False

def click_redo(driver):
    """Looks for the Redo/Restart button and clicks it."""
    print("Looking for Redo button...")
    try:
        # Wait specifically for the 'Redo' button to be clickable.
        redo_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Redo')] | //div[contains(@class, 'js-restart')]"))
        )
        redo_btn.click()
        print("Clicked Redo. Restarting...")
        time.sleep(2) # Wait for animation
        return True
    except:
        return False

def main():
    driver = setup_driver()
    
    # 1. Open the website
    driver.get("https://www.typing.com/student/lesson/35/numeric-keypad-10-key")
    
    print("-" * 30)
    print("INSTRUCTIONS:")
    print("1. Log in manually if required.")
    print("2. Navigate to the typing test screen.")
    print("3. Click inside the browser window to ensure it's active.")
    input("4. Press ENTER here in the console when you are ready to start the bot... ")
    print("-" * 30)

    # Main Automation Loop
    while True:
        # Step 1: Type the content
        finished_typing = type_numbers(driver)
        
        # Step 2: If typing finished, look for the Redo button indefinitely until found
        if finished_typing:
            while True:
                if click_redo(driver):
                    break # Break the wait loop to go back to typing
                time.sleep(1) # Check every second for the button
        
        time.sleep(2)

if __name__ == "__main__":
    main()