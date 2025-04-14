import os
import time
import psutil
from mailjet_rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")

# Access the API secret 
api_secret = os.getenv("API_SECRET")

# Define system time
current_time = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S",current_time)

# Define System thresholds ( 10% RAM, 50% free disk space, 10% CPU )
CPU_THRESHOLD = 2
RAM_THRESHOLD = 10
DISK_THRESHOLD = 50

# function to send email alert
def send_alert(subject, message):
    # instantiate mailjet client
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
            "From": {
                "Email": "your email address",
                "Name": "24/7 SysMon"
            },

            "To": [
                {
                "Email": "recipient email address",
                "Name": "Admin"
                }
             ],

            "Subject": subject,
            "HTMLPart": f"<h3>{message}</h3>"
           }
         ]
    }
    
    try:
        result = mailjet.send.create(data=data)
        print(f"Email sent: {result.status_code}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


# Check system metrics
cpu_usage = psutil.cpu_percent(interval=1)
# print(cpu_usage)
ram_usage = psutil.virtual_memory().percent
# print(ram_usage)
disk_usage = psutil.disk_usage('/').percent
# print(disk_usage)

#Create a store for email message
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