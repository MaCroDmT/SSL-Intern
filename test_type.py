import pyautogui
import time

print("--- TEST STARTING ---")
print("Switch to your browser NOW. I will type '4' in 3 seconds.")
time.sleep(5)

print("Typing now...")
pyautogui.write("4")
pyautogui.press("enter")
print("--- TEST FINISHED ---")