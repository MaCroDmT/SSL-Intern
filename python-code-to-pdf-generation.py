from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

# Get user's Downloads folder
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
pdf_file = os.path.join(downloads_path, "Employee_Monitoring_User_Manual.pdf")

c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4
margin = 50
line_height = 14
y = height - margin

def write_line(text, indent=0):
    global y
    c.drawString(margin + indent, y, text)
    y -= line_height

# Title
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(width/2, y, "Employee Monitoring App – User Manual")
y -= 30

c.setFont("Helvetica", 12)

write_line("Overview")
write_line("The Employee Monitoring App is a simple desktop application that automatically captures screenshots")
write_line("of your computer at regular intervals and saves them safely. The app also allows you to pause or stop")
write_line("the monitoring at any time. When stopped, the app creates a ZIP file of today’s screenshots in your Downloads folder.")
y -= 10

write_line("System Requirements")
write_line("• Windows 10 or later")
write_line("• At least 100 MB of free disk space")
write_line("• No need to install Python or any other software")
y -= 10

write_line("How to Use the App")
write_line("1. Start Monitoring")
write_line("   - Click the 'Start' button. The app will take a screenshot every 5 minutes.")
write_line("2. Pause Monitoring")
write_line("   - Click 'Pause' to temporarily stop capturing.")
write_line("3. Stop Monitoring")
write_line("   - Click 'Stop' to stop capturing and automatically create a ZIP file of today's screenshots")
write_line("     in your Downloads folder.")
y -= 10

write_line("Access Screenshots")
write_line("• Individual screenshots remain in the 'screenshots' folder located next to the .exe file.")
write_line("• The ZIP file will be in your Downloads folder, named like: screenshots_YYYYMMDD.zip")
y -= 10

write_line("Tips and Notes")
write_line("• Keep the app running to capture screenshots.")
write_line("• You can move the .exe file anywhere; the screenshots folder will be created automatically.")
write_line("• Only today's screenshots are added to the ZIP file automatically.")
y -= 10

write_line("Troubleshooting")
write_line("• App doesn’t start / Windows warning → Click 'More info → Run anyway'")
write_line("• Screenshots not being captured → Make sure Start was clicked and app window is open")
write_line("• ZIP file not in Downloads → Check disk space and permissions")
y -= 10

write_line("For any kind of assistance, please feel free to email at: prottoy.saha@soniagroup.com")
write_line("Or find me at Microsoft Teams")
y -= 10

write_line("Developed By:")
write_line("Prottoy Saha")
write_line("Phone: +8801745547578")
write_line("IT Intern")
write_line("Sonia and Sweaters LTD (SSL)")

# Save PDF
c.save()
print(f"PDF generated successfully in Downloads folder: {pdf_file}")
