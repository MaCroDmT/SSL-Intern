import pyautogui
import time
import os
import json
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
# PASTE YOUR API KEY HERE
API_KEY = "AIzaSyDPhlcURkrrjQduM0lYy4DIEzT2FT8KEKU" 

# Configure the AI
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

# Safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

def analyze_screen_with_ai():
    """
    Takes a screenshot and asks Gemini 2.5 Flash to find the Redo button.
    It strictly differentiates between the Yellow Continue button and Grey Redo button.
    """
    print("[AI] Analyzing screen...", end='\r')
    
    # 1. Take Screenshot
    screenshot_path = "screen_temp.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    
    # 2. Strict Prompt for Visual Differentiation
    prompt = """
    Look at this screen. I am playing a typing game. The round has finished.
    I need to find the "Redo" or "Retry" button to start over.
    
    CRITICAL VISUAL RULES:
    1. There is a "Continue" button that is usually YELLOW or Orange. IGNORE IT. DO NOT CLICK IT.
    2. There is a "Redo" button that is usually a GREY Icon (circular arrow) or text. FIND THIS ONE.
    
    Task:
    - Return the center X and Y coordinates of the REDO button.
    - If you only see the Yellow Continue button, return "found": false.
    
    Return JSON ONLY:
    {"found": true, "x": 123, "y": 456}
    OR
    {"found": false}
    """

    try:
        # 3. Upload and Generate
        file = genai.upload_file(screenshot_path)
        result = model.generate_content([prompt, file])
        
        # 4. Parse JSON
        response_text = result.text.strip()
        if "```" in response_text:
            response_text = response_text.replace("```json", "").replace("```", "")
        
        data = json.loads(response_text)
        
        # Cleanup
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
        return data
        
    except Exception as e:
        print(f"[AI Error] {e}")
        return {"found": False}

def main():
    print("--- AI SMART TYPER (Strict Mode) ---")
    if API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        print("ERROR: Please paste your Google Gemini API Key in the script!")
        return

    print("1. Go to the typing page.")
    print("2. Click inside the text box.")
    print("3. Starting in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\n--- RUNNING ---")
    
    while True:
        try:
            # PHASE 1: TYPE (The "Work" Phase)
            # We type for a specific amount of work, then we MUST stop to check.
            print("[ACTION] Typing batch... (Do not move mouse)      ", end='\r')
            
            # Type '4' + Enter repeatedly.
            # We do this in a loop to ensure we fill the page, but not forever.
            for _ in range(12): 
                pyautogui.write('4444444444', interval=0.005) 
                pyautogui.press('enter')
            
            # PHASE 2: STOP AND THINK (The "Intelligence" Phase)
            # We stop typing completely to let the AI look at the screen.
            print("\n[ACTION] Stopped typing. Checking screen...      ")
            
            # Brief pause to let the screen update if the game just finished
            time.sleep(1.0)
            
            ai_result = analyze_screen_with_ai()
            
            if ai_result and ai_result.get("found") == True:
                # AI found the Redo button!
                x = ai_result.get("x")
                y = ai_result.get("y")
                print(f"[AI] SUCCESS: Redo button found at ({x}, {y}). Clicking...")
                
                # Click the Redo button
                pyautogui.click(x, y)
                
                # Move mouse away to clear the view
                pyautogui.move(200, 0)
                
                # WAIT for the redirect/reload (Critical step)
                print("[WAIT] Waiting 5 seconds for page reload...")
                time.sleep(5.0)
                
                # Re-focus on the center (Typing box)
                screen_width, screen_height = pyautogui.size()
                pyautogui.click(screen_width/2, screen_height/2)
                print("[ACTION] Resuming typing loop.")
                
            else:
                # AI did not find the button, which means we are probably still in the middle of a game.
                # So we loop back and keep typing.
                print("[AI] Redo button not found. Continuing to type...")

        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            # If error, wait a bit and retry
            time.sleep(2)

if __name__ == "__main__":
    main()