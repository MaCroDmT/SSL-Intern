import xlwings as xw
from datetime import datetime
from tkinter import Tk, filedialog, messagebox, Button, Label
import os

# ---------------- RGB Colors ----------------
YELLOW = (255, 255, 153)   # 2 weeks away
RED = (255, 153, 153)      # 1 week away
RED_FONT = (156, 0, 6)     # Deadline passed
BLACK = (0, 0, 0)          # Normal text

def rgb_to_int(rgb_tuple):
    """Convert (R,G,B) to Excel RGB integer"""
    r, g, b = rgb_tuple
    return b << 16 | g << 8 | r

# ---------------- Excel Processing ----------------
def process_excel(file_path):
    app = xw.App(visible=False)
    wb = app.books.open(file_path)

    today = datetime.today().date()

    for ws in wb.sheets:
        used_range = ws.used_range
        for cell in used_range:
            value = cell.value
            if value is None:
                continue

            parsed_date = None

            # Case 1: datetime object
            if isinstance(value, datetime):
                parsed_date = value.date()
            # Case 2: string like "6-Aug" or "2025-08-06"
            elif isinstance(value, str):
                try:
                    parsed_date = datetime.strptime(value, "%d-%b").date().replace(year=today.year)
                except:
                    try:
                        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                    except:
                        continue
            else:
                continue

            days_left = (parsed_date - today).days

            # Apply formatting rules
            if days_left < 0:
                # Passed deadline → red text only
                cell.api.Font.Color = rgb_to_int(RED_FONT)
                cell.api.Interior.ColorIndex = 0  # no background
            elif days_left <= 7:
                # Within 1 week → red cell
                cell.api.Interior.Color = rgb_to_int(RED)
                cell.api.Font.Color = rgb_to_int(BLACK)
            elif days_left <= 14:
                # Within 2 weeks → yellow cell
                cell.api.Interior.Color = rgb_to_int(YELLOW)
                cell.api.Font.Color = rgb_to_int(BLACK)
            # else → more than 2 weeks → do nothing

    # Save processed file
    base, ext = os.path.splitext(file_path)
    safe_base = base.replace(" ", "_")
    output_file = safe_base + "_Formatted" + ext
    wb.save(output_file)
    wb.close()
    app.quit()
    return output_file

# ---------------- GUI ----------------
def choose_file():
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xlsm *.xltx *.xltm")]
    )
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return
    try:
        output_file = process_excel(file_path)
        messagebox.showinfo("Success", f"File processed successfully!\nSaved as:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def main():
    root = Tk()
    root.title("Deadline Highlighter")
    root.geometry("350x150")

    Label(root, text="Excel Deadline Highlighter", font=("Arial", 14, "bold")).pack(pady=10)
    Button(root, text="Select Excel File", command=choose_file, width=25, height=2).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
