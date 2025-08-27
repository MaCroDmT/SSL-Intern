import tkinter as tk
from tkinter import messagebox
import datetime

def get_religious_holidays(year):
    """
    Returns a dictionary of religious holidays for a given year.
    Note: These dates are approximations and may vary.
    """
    holidays = {
        2025: {
            "Eid-ul-Fitr": datetime.date(2025, 3, 31),
            "Eid-ul-Adha": datetime.date(2025, 6, 7),
            "Durga Puja": datetime.date(2025, 10, 1),
            "Buddha Purnima": datetime.date(2025, 5, 12),
            "Christmas Day": datetime.date(2025, 12, 25),
            "Ashura": datetime.date(2025, 7, 6),
            "Easter Sunday": datetime.date(2025, 4, 20),
            "Shab-e-Barat": datetime.date(2025, 3, 15),
            "Shab-e-Qadr": datetime.date(2025, 4, 25),
            "Janmashtami": datetime.date(2025, 8, 15),
            "Prophet's Birthday": datetime.date(2025, 9, 5)
        },
        2026: {
            "Eid-ul-Fitr": datetime.date(2026, 3, 20),
            "Eid-ul-Adha": datetime.date(2026, 5, 27),
            "Durga Puja": datetime.date(2026, 10, 20),
            "Buddha Purnima": datetime.date(2026, 5, 1),
            "Christmas Day": datetime.date(2026, 12, 25),
            "Ashura": datetime.date(2026, 6, 25),
            "Easter Sunday": datetime.date(2026, 4, 5),
            "Shab-e-Barat": datetime.date(2026, 3, 5),
            "Shab-e-Qadr": datetime.date(2026, 4, 15),
            "Janmashtami": datetime.date(2026, 9, 4),
            "Prophet's Birthday": datetime.date(2026, 8, 25)
        }
    }
    return holidays.get(year, {})

def is_peak_season(date):
    """Checks if a given date falls within the peak season (March to August)."""
    return 3 <= date.month <= 8

def calculate_holidays():
    """
    Calculates and displays the holiday forecast based on GUI inputs.
    """
    MAX_HOLIDAYS = 11
    
    try:
        year = int(year_entry.get())
        given_holidays = int(holidays_entry.get())
        
        if not (0 <= given_holidays <= MAX_HOLIDAYS):
            messagebox.showerror("Invalid Input", f"Please enter a number between 0 and {MAX_HOLIDAYS} for given holidays.")
            return

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for the year and holidays.")
        return

    # --- Get and sort holidays for the specified year ---
    all_holidays = get_religious_holidays(year)
    if not all_holidays:
        messagebox.showinfo("No Data", f"No holiday data available for the year {year}. Exiting.")
        return

    sorted_holidays = sorted(all_holidays.items(), key=lambda item: item[1])

    holidays_to_give = MAX_HOLIDAYS - given_holidays
    given_holiday_list = []
    output_text.delete(1.0, tk.END)  # Clear previous results

    output_text.insert(tk.END, f"--- Holiday Decision for {year} ---\n")
    output_text.insert(tk.END, f"Total religious holidays to be given: {holidays_to_give}\n\n")

    if holidays_to_give > 0:
        # --- Separate holidays into peak and non-peak season lists ---
        peak_season_holidays = [h for h in sorted_holidays if is_peak_season(h[1])]
        non_peak_season_holidays = [h for h in sorted_holidays if not is_peak_season(h[1])]

        # --- Peak Season Logic (March - August) ---
        output_text.insert(tk.END, "**Peak Season (March - August) Rules Applied:**\n")
        
        for holiday_name, holiday_date in peak_season_holidays:
            if holidays_to_give > 0:
                given_holiday_list.append((holiday_name, holiday_date))
                holidays_to_give -= 1
            else:
                break
        
        # --- Non-Peak Season Logic (Remaining months) ---
        output_text.insert(tk.END, "\n**Non-Peak Season Rules Applied:**\n")
        
        for holiday_name, holiday_date in non_peak_season_holidays:
            if holidays_to_give > 0:
                given_holiday_list.append((holiday_name, holiday_date))
                holidays_to_give -= 1
            else:
                break

        # --- Display the final list ---
        if given_holiday_list:
            final_list = sorted(given_holiday_list, key=lambda item: item[1])
            output_text.insert(tk.END, "\nFinal List of Holidays to be given:\n")
            for holiday_name, holiday_date in final_list:
                season_info = "Peak Season" if is_peak_season(holiday_date) else "Non-Peak Season"
                # The line below is the key change to add the weekday name
                formatted_date = holiday_date.strftime('%A, %B %d, %Y')
                output_text.insert(tk.END, f"- {holiday_name}: {formatted_date} ({season_info})\n")
    else:
        output_text.insert(tk.END, "\nNo more holidays need to be given.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Holiday Calendar Forecast")
root.geometry("500x400")

# Input Frame
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack()

# Year Input
tk.Label(input_frame, text="Enter the year:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
year_entry = tk.Entry(input_frame, width=15, font=("Helvetica", 12))
year_entry.grid(row=0, column=1, padx=5, pady=5)
year_entry.insert(0, str(datetime.datetime.now().year))

# Holidays Given Input
tk.Label(input_frame, text="Holidays already given (0-11):", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
holidays_entry = tk.Entry(input_frame, width=15, font=("Helvetica", 12))
holidays_entry.grid(row=1, column=1, padx=5, pady=5)
holidays_entry.insert(0, "0")

# Button to trigger calculation
calculate_button = tk.Button(root, text="Calculate Holidays", command=calculate_holidays, font=("Helvetica", 12, "bold"))
calculate_button.pack(pady=10)

# Output Textbox
output_text = tk.Text(root, height=15, width=60, font=("Helvetica", 10), state=tk.NORMAL)
output_text.pack(padx=10, pady=10)

root.mainloop()