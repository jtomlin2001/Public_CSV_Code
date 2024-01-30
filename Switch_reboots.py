import meraki
import requests
import subprocess
import datetime
import time
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import requests
import json



txt = open("Switch Reboot Status.txt","w+")

base_url = 'https://api.meraki.com/api/v1'
session_params = {
    'api_key': api_key,
    'base_url': base_url,

}
dashboard = meraki.DashboardAPI(**session_params)
headers = {
        'X-Cisco-Meraki-API-Key': api_key
    }
network_devices = []
device = []
organization_id = '445912'
networks = dashboard.organizations.getOrganizationNetworks(organization_id)

for network in networks:
    network_id = network['id']
    network_name = network['name']
    response = dashboard.networks.getNetworkDevices(network_id)
    for switch in response:
        if switch['model'].startswith("MS"):
            txt = open("Switch Reboot Status.txt","a")
            serial = switch['serial']
            name = (switch['name'])
            reboot = requests.post(f"{base_url}/devices/{serial}/reboot", headers={'Authorization': f'Bearer {api_key}'})
            print(reboot.status_code)
            if reboot.status_code == 202:
                status = "Successfully Rebooted!"
            else:
                status = "Failed"
            txt.write(f"{name}--->{status}\n")
            
            
smtp_server = 'hqsmtp01.clinicasierravista.org'
smtp_port = 25
sender_email = 'automation@clinicasierravista.org'
recipient_email = 'infrastructure@clinicasierravista.org'
subject = 'Switch Reboot API Confirmation'
if status == "Successfully Rebooted!":
    body = '<span style="font-size: 27px;">All Switches Have Been Rebooted Successfully!</span><br><br>'
    body += '<ul style="font-size: 21px;">See attached logs for more info.</ul><br>'
else:
    body = '<span style="font-size: 27px;">There was an error please review attached logs</span><br><br>'
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
    <body style = "font-size = 17px;">
    <div class="signature">
    <br><br>
      <p><span class="name">CSV Automation</span></p>
      <p><span class="email">Contact Email: jacob.tomlin@clinicasierravista.org </span></p>
      <p><span class="website"><a href="https://csv-it.org/">Visit our website</a></span></p>
    </div>
    </body>
    </html>
    """
msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.add_alternative(body + signature, subtype='html')
with open('Switch Reboot Status.txt', 'rb') as f:
    file_data = f.read()
msg.add_attachment(file_data, maintype='text', subtype='plain', filename='Reboot_Logs.txt')
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.send_message(msg)