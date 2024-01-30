import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import meraki
import requests
from time import sleep

smtp_port = 25
sender_email = 'automation@clinicasierravista.org'
recipient_email = 'infrastructure@clinicasierravista.org'
subject = 'CSV Wireless set to be removed in 30 minutes '
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
header = (f'<span style="font-size: 27px;">In the unlikely event you need to abort the scheduled task</span><br><br>')
body = '<span style="font-size: 20px;">RDP into csvapp03, hit windows key, search "task scheduler", and end the task named "CSV Wireless Remover" in the task scheduler. See attached image for more info</span><br><br>'
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
body += f"""
<img src="cid:image1">  <!-- This is where you reference the image -->
<p><span class="website" style="font-size: 16px;"><a href="https://csv-it.org/wireless_bomber/">After ending the task to manually send the job click this link *requires admin</a></span></p>
"""

# Attach the HTML content
msg.attach(MIMEText(header + body + signature, 'html'))

# Load and attach the PNG image
with open('C:\\Users\\so_tomlinj\\Pictures\\Kill_CSV_Task.png', 'rb') as fp:
    img = MIMEImage(fp.read(), name='image.png')
    img.add_header('Content-ID', '<image1>')  # Set the image ID to match the reference in the HTML
    msg.attach(img)
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.send_message(msg)

sleep(1800)
output_messages = []

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

organization_id = '445912'
networks = dashboard.organizations.getOrganizationNetworks(organization_id)
network_count = len(networks)
networks_done = 0

for network in networks:
    network_id = network['id']
    response = requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids", headers=headers)
    if response.status_code == 200:
        ssids = response.json()
        for ssid in ssids:
            if ssid['name'] == "CSV Wireless":
                ssid_num = ssid['number']
        if ssid_num >= 0: 
            ssid_get = requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids/{ssid_num}", headers=headers)
            if ssid_get.status_code == 200:
                output_messages.append(f"Found CSV Wireless at {network['name']}")
                ssid_info = ssid_get.json()
                ssid_info['enabled'] = False
                ssid_info['enabled'] = False
                ssid_info['dot11w'] = {}
                ssid_info['dot11r'] = {}
                ssid_info['activeDirectory'] ={}
                ssid_info['speedBurst'] = {}
                ssid_put = requests.put(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids/{ssid_num}", headers=headers, data=ssid_info)
                if ssid_put.status_code == 200:
                    output_messages.append(f"{network['name']} : Successfully Removed")
                    networks_done += 1
                    
                else: 
                    output_messages.append(f"Error Removing CSV Wireless from {network['name']}")
        else:
            output_messages.append(f"Could not find CSV Wireless on {network['name']}")
subject2 = 'CSV Wireless Removed'            
header2 = (f'<span style="font-size: 27px;">Script Results</span><br><br>')
body2 = '<span style="font-size: 25px;">Site Name: Status</span><br><br>'
output = ''
#for message in output_messages:
#    output += (f'<p style="font-size: 17px;">{message}</p> <br>')
msg2 = EmailMessage()
msg2['From'] = sender_email
msg2['To'] = recipient_email
msg2['Subject'] = subject2
msg2.add_alternative(header2 + body2  + output + signature, subtype='html')
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.send_message(msg2)