import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
import meraki
import requests
from time import sleep

smtp_port = 25
sender_email = 'automation@clinicasierravista.org'
recipient_email = 'infrastructure@clinicasierravista.org'
subject = 'Clients Not Reaching DHCP'
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

organization_id = '445912'
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
                if client['ip']:
                    if client['ip'].startswith("169") and network['name']:
                        staff_client_count += 1
                        device_info.append(f"Site: {network['name']} | Device ID:{client['id']} | Device OS:{client['os']} | Device User:{client['user']} | Device IP:{client['ip']} | Device Mac:{client['mac']} | Device Description {client['description']}")
        else:
            pass
header = (f'<span style="font-size: 27px;">Searching active Clients</span><br><br>')
if staff_client_count:
    clients = (f'<span style="font-size: 24px;">{staff_client_count} APIPA Clients</span><br><br>')
    for device in device_info:
        clients += (f'<li style="font-size: 17px"> {device}</li>')
else:
    clients = (f'<span style="font-size: 24px;">No APIPA Clients Found</span><br><br>')
clients += '<br><br>'
msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.add_alternative(header + clients + signature, subtype='html')
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.send_message(msg)