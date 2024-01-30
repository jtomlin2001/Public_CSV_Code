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
subject = 'Nextgen VPN is down attempting redemption...'
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
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}
vpn_list = '''{
    "peers": [
                {
            "name": "NexGen",
            "privateSubnets": [ "192.168.146.0/24" ],
            "ikeVersion": "2",
            "networkTags": [ "all" ],
            "ipsecPoliciesPreset": "default"
        },
        {
            "name": "BofA to Azure",
            "privateSubnets": [ "172.25.2.0/24" ],
            "secret": "4UWv76gAZrY5",
            "ikeVersion": "1",
            "networkTags": [ "all" ],
            "ipsecPoliciesPreset": "azure"
        }
    ]
}'''

restart_list = '''{
    "peers": [
        {
            "name": "BofA to Azure",
            "privateSubnets": [ "172.25.2.0/24" ],
            "ikeVersion": "1",
            "networkTags": [ "all" ],
            "ipsecPoliciesPreset": "azure"
        }
    ]
}'''
url = "https://api.meraki.com/api/v1/organizations/445912/appliance/vpn/thirdPartyVPNPeers"
hostname = "192.168.146.20" 
response = os.system("ping -n 4 " + hostname)

if response == 0:
    print("is up")
else:
    response = requests.put(url, headers=headers, data = restart_list)
    if response.status_code == 200:
        sleep(10)
        up = requests.put(url, headers=headers, data=vpn_list)
        if up.status_code == 200:
            print(up.text)
            sleep(20)
            check = os.system("ping -n 4 192.168.146.20")
            count = 0
            while check != 0:
                print(count)
                if count < 10:
                    check = os.system("ping -n 4 192.168.146.20")
                    count += 1
                else:
                    count = 0
                    response = requests.put(url, headers=headers, data = restart_list)
                    if response.status_code == 200:
                        sleep(10)
                        up = requests.put(url, headers=headers, data=vpn_list)
                    if up.status_code == 200:
                        print(up.text)
            body = '<span style="font-size: 27px;">VPN Connection has been restored!</span><br><br>'
            msg = EmailMessage()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.add_alternative(body + signature, subtype='html')
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.send_message(msg)
            
    else:
        print()
            
                
    
    
    