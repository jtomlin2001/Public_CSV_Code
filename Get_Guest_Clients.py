import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from datetime import datetime
import os
import requests
from time import sleep

smtp_port = 25
sender_email = 'automation@clinicasierravista.org'
recipient_email = 'infrastructure@clinicasierravista.org'
signature = """
    <html>
    <head>
    <style>
    .signature {
      font-family: Arial, sans-serif;
      font-size: 17px;
      color: #333333;
    }
    
    .name {
      font-weight: bold;
    }
    .class{
    font-size: 64px;
    }
    .email {
      color: #666666;
      font-size: 17px;
    }
    
    .website {
      color: #0000FF;
      text-decoration: none;
    }
    </style>
    </head>
    <body>
    <div class="signature">
    <br><br>
      <p><span class="name">CSV Automation</span></p>
      <p><span class="email">Contact Email: jacob.tomlin@clinicasierravista.org </span></p>
      <p><span class="website"><a href="https://csv-it.org/">Visit our website</a></span></p>
    </div>
    </body>
    </html>
    """


base_url = 'https://api.meraki.com/api/v1'
session_params = {
    'api_key': api_key,
    'base_url': base_url,

}
headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json',
}
network_devices = []
device = []
tracker = 0
minutes = 0
time = str(datetime.now().strftime('%H:%M'))
current = int(time.replace(':',''))
while current != 700:
    current -= 1
    tracker += 1
    minutes += 1
    if tracker == 60:
        tracker = 0
        current -= 40
seconds = (minutes*60)
organization_id = '445912'
networks_url  = f'https://api.meraki.com/api/v1/organizations/{organization_id}/networks'
networks = requests.get(networks_url, headers=headers)
networks = (networks.json())
guest_client_count = 0
output_messages = []
device_info =[]

for network in networks:
    guest_site_count = 0
    network_id = network['id']
    response = requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/clients?timespan={seconds}&perPage=1000", headers=headers)
    if response.status_code == 200:
        clients = response.json()
        if clients:
            for client in clients:
                if client['ssid'] == "CSV Guest":
                    guest_client_count += 1
                    guest_site_count += 1
            print(f"Clients {guest_client_count}")
        else:
            pass
    output_messages.append(f"{network['name']}: ${round(guest_site_count * 0.0079, 3)}")
total = round(guest_client_count * 0.0079, 3)
subject = 'Twilio Cost'
header = '<span style="font-size: 27px;">Estimates are done daily and are calculate based on clients that have joined since 7am today</span><br><br>'
body = (f'<span style="font-size: 32px;">Total Current Cost: ${total}</span><br><br>')
sites = '<span style="font-size: 24px;">Per Site Breakdown</span><br><br>'
for message in output_messages:
    sites += (f'<p style="font-size: 17px;">{message}</p>')
msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.add_alternative(header + body + sites + signature, subtype='html')
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.send_message(msg)