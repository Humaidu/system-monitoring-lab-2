import os
import time
import psutil
import resend
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
resend.api_key = os.getenv("API_KEY")

if not resend.api_key:
    raise Exception("Missing RESEND_API_KEY in .env file")

# Define system time
current_time = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S",current_time)

# Define System thresholds ( 10% RAM, 50% free disk space, 10% CPU )
CPU_THRESHOLD = 2
RAM_THRESHOLD = 10
DISK_THRESHOLD = 50

# function to send email alert
def send_alert(subject, message):
    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": ["humaiduali@gmail.com"],
            "subject": subject,
            "html": f"<p>{message}</p>"
        })
        print("Email sent:", response["id"])
    except Exception as e:
        print("Failed to send email:", str(e))

# Check system metrics
cpu_usage = psutil.cpu_percent(interval=1)
ram_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent

# Create alert message based on threshold breaches
alert_message = ""
if cpu_usage > CPU_THRESHOLD:
    alert_message += f"CPU usage is high: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)\n"

if ram_usage > RAM_THRESHOLD:
    alert_message += f"RAM usage is high: {ram_usage}% (Threshold: {RAM_THRESHOLD}%)\n"

if disk_usage > DISK_THRESHOLD:
    alert_message += f"Disk space is low: {100 - disk_usage}% free (Threshold:{DISK_THRESHOLD}% free)\n"

# If any threshold is breached, send an email alert
if alert_message:
    send_alert(f"Python Monitoring Alert Alert-{formatted_time}", alert_message)
else:
    print("All system metrics are within normal limits.")