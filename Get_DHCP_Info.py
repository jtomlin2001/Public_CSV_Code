import meraki
import requests
import ipaddress
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

smtp_port = 25
sender_email = 'automation@clinicasierravista.org'
recipient_email = 'infrastructure@clinicasierravista.org'
subject = '🚨 WARNING DHCP Scopes Reaching High Utilization! 🚨'
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

headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json',
}
base_url = 'https://api.meraki.com/api/v1'
session_params = {
    'api_key': api_key,
}
dashboard = meraki.DashboardAPI(**session_params)
organization_id = '445912'
networks = dashboard.organizations.getOrganizationNetworks(organization_id)
header = (f'<span style="font-size: 27px;">Scopes approaching high utlization:</span><br><br>')
body =''
vlans_over = 0
for network in networks:
    network_id = network['id']
    res = requests.get(f"{base_url}/networks/{network_id}/clients?statuses[]=Online&perPage=1000", headers=headers)
    clients = res.json() if res.status_code == 200 else []
    net_name = str({network['name']})
    network_name = net_name.strip("}{'")
    print(network_name)
    if clients:
        resp = requests.get(f"{base_url}/networks/{network_id}/appliance/vlans", headers=headers)
        vlans = resp.json() if resp.status_code == 200 else []
        available_ips = {} 
        info = {} 
        blacklist= ["Lumen MPLS", "Default", "Uplink to Cisco Router", "PolyCom","MPLS"]
        for vlan in vlans:
            subnet = vlan['subnet']
            if vlan['name'] not in blacklist:
                subnet_info = ipaddress.IPv4Network(subnet)
                all_ips = [str(ip) for ip in subnet_info.hosts()]
                client_ip = [client['ip'] for client in clients]
                available_ips[vlan['name']] = [ip for ip in all_ips if ip not in client_ip]
                used_count = (len(all_ips)) - len(available_ips[vlan['name']])
                percentage_used = ((used_count+5) / len(all_ips)) * 100
                subnet_used_percentage = round(percentage_used, 2)
                if subnet_used_percentage > 90:
                    vlans_over += 1
                    vlan_name = (vlan['name'])
                    body += (f'<span style="font-size: 25px;"<h1>Site Name: {network_name}</h1><br><br>')
                    body += (f'<span style="font-size: 22px;"<li>Vlan Name: {vlan_name}</li><br><br>')
                    body += (f'<span style="font-size: 22px;"<ul>Subnet Usage: {subnet_used_percentage}%</ul><br><br>')
if vlans_over:
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.add_alternative(header + body + signature, subtype='html')
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.send_message(msg)