import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
import meraki
import requests
from time import sleep
smtp_server = 'hqsmtp01.clinicasierravista.org'
smtp_port = 25
sender_email = 'automation@clinicasierravista.org'
recipient_email = 'infrastructure@clinicasierravista.org'
subject = 'Wireless Client Breakdown'
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
dashboard = meraki.DashboardAPI(**session_params)
headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json',
}
network_devices = []
device = []

networks = dashboard.organizations.getOrganizationNetworks(organization_id)
staff_client_count = 0
wireless_client_count = 0
iot_client_count = 0
guest_client_count = 0
output_messages = []
device_info =[]

for network in networks:
    staff_site_count = 0
    wireless_site_count = 0
    iot_site_count = 0
    guest_site_count = 0
    network_id = network['id']
    response = requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/clients?statuses[]=Online&perPage=1000", headers=headers)
    if response.status_code == 200:
        clients = response.json()
        if clients:
            for client in clients:
                if client['ssid'] == "CSV Staff":
                    staff_client_count += 1
                    staff_site_count += 1
                elif client['ssid'] == "CSV Wireless":
                    device_info.append(f"Site: {network['name']} | Device ID:{client['id']} | Device OS:{client['os']} | Device User:{client['user']}")
                    wireless_client_count += 1
                    wireless_site_count += 1
                elif client['ssid'] == "CSV IOT":
                    iot_client_count += 1
                    iot_site_count += 1
                elif client['ssid'] == "CSV Guest":
                    guest_client_count += 1
                    guest_site_count += 1
        else:
            pass
    output_messages.append(f"{network['name']}:     CSV Staff-{staff_site_count}  CSV Wireless-{wireless_site_count}  CSV IOT-{iot_site_count}    CSV Guest-{guest_site_count}")
header = (f'<span style="font-size: 27px;">Total Current Wireless Clients: {staff_client_count+wireless_client_count+iot_client_count+guest_client_count}</span><br><br>')
body = '<span style="font-size: 25px;">Per SSID Breakdown</span><br><br>'
body += (f'<span style="font-size: 22px"<li>CSV Staff: {staff_client_count}</li><br><br>')
body += (f'<li>CSV Wireless: {wireless_client_count}</li><br><br>')
body += (f'<li>CSV IOT: {iot_client_count}</li><br><br>')
body += (f'<li>CSV Guest: {guest_client_count}</li><br><br></span>')
clients = '<span style="font-size: 24px;">CSV Wireless Clients Details</span><br><br>'
sites = '<span style="font-size: 24px;">Per Site Breakdown</span><br><br>'
for device in device_info:
    clients += (f'<li style="font-size: 17px"> {device}</li>')
for message in output_messages:
    sites += (f'<p style="font-size: 17px;">{message}</p>')
clients += '<br><br>'
msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.add_alternative(header + body + clients + sites + signature, subtype='html')
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.send_message(msg)