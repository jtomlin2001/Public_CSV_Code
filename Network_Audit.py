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


# File paths
sslvpn_users_file = r"\\csvfile01\IT\Network\Quarterly Audit\ASA Firewall\SSLVPN-users.csv"
so_asa_file = r"\\csvfile01\IT\Network\Quarterly Audit\ASA Firewall\SO_ASA.csv"
cisco_file = r"\\csvfile01\IT\Network\Quarterly Audit\Cisco\cisco.csv"
sslvpn_users_file_new = r"\\csvfile01\IT\Network\Quarterly Audit\ASA Firewall\SSLVPN-users_new.csv"
so_asa_file_new = r"\\csvfile01\IT\Network\Quarterly Audit\ASA Firewall\SO_ASA_new.csv"
cisco_file_new = r"\\csvfile01\IT\Network\Quarterly Audit\Cisco\cisco_new.csv"
meraki_admin_list_file = r"\\csvfile01\IT\Network\Quarterly Audit\Meraki\meraki_admin_list.csv"
meraki_read_list_file = r"\\csvfile01\IT\Network\Quarterly Audit\Meraki\meraki_read_list.csv"
meraki_tech_list_file = r"\\csvfile01\IT\Network\Quarterly Audit\Meraki\meraki_tech_list.csv"
meraki_admin_list_file_new = r"\\csvfile01\IT\Network\Quarterly Audit\Meraki\meraki_admin_list_new.csv"
meraki_read_list_file_new = r"\\csvfile01\IT\Network\Quarterly Audit\Meraki\meraki_read_list_new.csv"
meraki_tech_list_file_new = r"\\csvfile01\IT\Network\Quarterly Audit\Meraki\meraki_tech_list_new.csv"

def run_powershell_command(command):
    completed_process = subprocess.run(["powershell", "-Command", command], capture_output=True)
    output = completed_process.stdout.decode("utf-8").strip()
    print(output)
    return output


def send_notification_email(soList, sslList, ciscoList, merakiAList, merakiRList, merakiTList):
    # Email configuration

    smtp_port = 25
    sender_email = 'automation@clinicasierravista.org'
    recipient_email = 'infrastructure@clinicasierravista.org'
    subject = 'Quarterly Network Access Audit'
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
    if soList or sslList or ciscoList or merakiAList or merakiRList or merakiTList:
        # Email subject and body
        body = '<span style="font-size: 27px;">The following changes have occurred since the last Network Access Audit:</span><br><br>'
        if soList:
            body += '<span style="font-size: 25px;">New groups detected in SO_ASA connected to the firewall:</span><br>'
            body += '<ul style="font-size: 21px;">'
            body += '<li>' + '</li><li>'.join(soList) + '</li>'
            body += '</ul><br>'
        if sslList:
            body += '<span style="font-size: 25px;">New users detected in SSLVPN-users connected to the firewall:</span><br>'
            body += '<ul style="font-size: 21px;">'
            body += '<li>' + '</li><li>'.join(sslList) + '</li>'
            body += '</ul><br>'
        if ciscoList:
            body += '<span style="font-size: 25px;">New groups detected in RADIUS:</span><br>'
            body += '<ul style="font-size: 21px;">'
            body += '<li>' + '</li><li>'.join(ciscoList) + '</li>'
            body += '</ul><br>'
        if merakiAList:
            body += '<span style="font-size: 25px;">New users detected in Meraki Admins:</span><br>'
            body += '<ul style="font-size: 21px;">'
            body += '<li>' + '</li><li>'.join(merakiAList) + '</li>'
            body += '</ul><br>'
        if merakiRList:
            body += '<span style="font-size: 25px;">New users detected in Meraki Read Only:</span><br>'
            body += '<ul style="font-size: 21px;">'
            body += '<li>' + '</li><li>'.join(merakiRList) + '</li>'
            body += '</ul><br>'
        if merakiTList:
            body += '<span style="font-size: 25px;">New users detected in Meraki Techs:</span><br>'
            body += '<ul style="font-size: 21px;">'
            body += '<li>' + '</li><li>'.join(merakiTList) + '</li>'
            body += '</ul><br>'
        # Create the email message
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.add_alternative(body + signature, subtype='html')
        with open(sslvpn_users_file, 'rb') as attachment:
            msg.add_attachment(attachment.read(), maintype='application', subtype='csv', filename="SSLVPN-users.csv")
        with open(so_asa_file, 'rb') as attachment1:
            msg.add_attachment(attachment1.read(), maintype='application', subtype='csv', filename="SO_ASA.csv")
        with open(cisco_file, 'rb') as attachment2:
            msg.add_attachment(attachment2.read(), maintype='application', subtype='csv', filename="Cisco_Radius.csv")
        with open(meraki_admin_list_file, 'rb') as attachment3:
            msg.add_attachment(attachment3.read(), maintype='application', subtype='csv', filename="Meraki_Admin.csv")
        with open(meraki_read_list_file, 'rb') as attachment4:
            msg.add_attachment(attachment4.read(), maintype='application', subtype='csv', filename="Meraki_Read_Only.csv")
        with open(meraki_tech_list_file, 'rb') as attachment5:
            msg.add_attachment(attachment5.read(), maintype='application', subtype='csv', filename="Meraki_Tech.csv")
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.send_message(msg)
            print("Notification email sent.")
        except Exception as e:
            print("Error sending notification email:", str(e))
    else:
        body = '<span style="font-size: 27px;">There have been no changes since the last Network Access Audit:</span><br><br>'
        # Create the email message
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        # Add the email signature
        msg.add_alternative(body + signature, subtype='html')
        with open(sslvpn_users_file, 'rb') as attachment:
            msg.add_attachment(attachment.read(), maintype='application', subtype='csv', filename="SSLVPN-users.csv")
        with open(so_asa_file, 'rb') as attachment1:
            msg.add_attachment(attachment1.read(), maintype='application', subtype='csv', filename="SO_ASA.csv")
        with open(cisco_file, 'rb') as attachment2:
            msg.add_attachment(attachment2.read(), maintype='application', subtype='csv', filename="Cisco_Radius.csv")
        with open(meraki_admin_list_file, 'rb') as attachment3:
            msg.add_attachment(attachment3.read(), maintype='application', subtype='csv', filename="Meraki_Admin.csv")
        with open(meraki_read_list_file, 'rb') as attachment4:
            msg.add_attachment(attachment4.read(), maintype='application', subtype='csv', filename="Meraki_Read_Only.csv")
        with open(meraki_tech_list_file, 'rb') as attachment5:
            msg.add_attachment(attachment5.read(), maintype='application', subtype='csv', filename="Meraki_Tech.csv")
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.send_message(msg)
        except Exception as e:
            print("Error sending notification email:", str(e))
        print("No items in the lists. Notification email sent.")
    #### Add cisco audit info
def asa_csv_reader():
    run_powershell_command(f'Get-ADGroupMember -Identity SSLVPN-users | Select-Object name | Out-File "{sslvpn_users_file_new}" -Encoding "utf8"')
    sslList = []
    soList = []
    with open(sslvpn_users_file, 'r') as old, open (sslvpn_users_file_new, 'r') as new:
        sslOne = old.readlines()
        sslTwo = new.readlines()
    with open(sslvpn_users_file, 'a') as one:
        for line in sslTwo:
            if line not in sslOne:
                if line.startswith("name"):
                    pass
                elif line.startswith("ï»¿"):
                    pass
                elif line.strip() == "":
                    pass
                else:
                    one.write(line)
                    print(f'New data detected adding {line.strip()} to csv')
                    sslList.append(line.strip())
    print("SSL VPN Users file read")
    run_powershell_command(f'Get-ADGroupMember -Identity SO_ASA | Select GivenName, SAMAccountName | Out-File "{so_asa_file_new}" -Encoding "utf8"')
    with open(so_asa_file, 'r') as old, open (so_asa_file_new, 'r') as new:
        soOne = old.readlines()
        soTwo = new.readlines()
    with open(so_asa_file, 'a') as one:
        for line in soTwo:
            if line not in soOne:
                if line.startswith("name"):
                    pass
                elif line.startswith("ï»¿"):
                    pass
                elif line.startswith("SAM"):
                    pass
                elif line.startswith("Given"):
                    pass
                elif line.strip() == "":
                    pass
                else:
                    one.write(line)
                    print(f'New data detected adding "{line.strip()}" to csv')
                    soList.append(line.strip())                 
    print("SO_ASA groups read")
    os.remove(sslvpn_users_file_new)
    os.remove(so_asa_file_new)
    return {'soList': soList, 'sslList': sslList}
def cisco_csv_reader():
        run_powershell_command(f'Get-ADGroupMember -Identity RADIUS-CiscoDevices| Select GivenName, SAMAccountName | Out-File "{cisco_file_new}" -Encoding "utf8"')
        ciscoList =[]
        with open(cisco_file, 'r')as old, open (cisco_file_new, 'r') as new:
            ciscoOne = old.readlines()
            ciscoTwo = new.readlines()
        with open(cisco_file, 'a') as one:
            for line in ciscoTwo:
                if line not in  ciscoOne:
                    if line.startswith("name"):
                        pass
                    elif line.startswith("ï»¿"):
                        pass
                    elif line.strip() == "":
                        pass
                    elif line.startswith("GivenName"):
                        pass
                    else:
                        one.write(line)
                        print(f'New data adding "{line.strip()}"')
                        ciscoList.append(line.strip())
        print("Cisco Radius groups read")
        os.remove(cisco_file_new)
        return {'ciscoList' : ciscoList}
def meraki_csv_reader():



    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    graph_api_url = 'https://graph.microsoft.com/v1.0/groups'

    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }

    response = requests.post(token_url, data=token_data)
    response.raise_for_status()  # Check if the token request was successful

    access_token = response.json()['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    group_ids = [
        '440d5980-851b-4413-80ca-d042d805ec63',
        'd776fb42-48cb-4266-8091-f874d806fb8e',
        '01da512c-cd68-48c2-b248-3062c910819c'
    ]
    group_user_names = {}
    for group_id in group_ids:
        if group_id == '440d5980-851b-4413-80ca-d042d805ec63':
            read_group_id = 'meraki_read'
        elif group_id == 'd776fb42-48cb-4266-8091-f874d806fb8e':
            read_group_id = 'meraki_admin'
        elif group_id == '01da512c-cd68-48c2-b248-3062c910819c':
            read_group_id = 'meraki_tech'
        group_api_url = f'{graph_api_url}/{group_id}/members'
        response = requests.get(group_api_url, headers=headers)
        response.raise_for_status()  # Check if the group members request was successful
        group_user_names[read_group_id] = []
        group_members_data = response.json().get('value')
        for member in group_members_data:
            group_user_names[read_group_id].append(member['displayName'])
    meraki_admin_list = (group_user_names['meraki_admin'])
    meraki_read_list = (group_user_names['meraki_read'])
    meraki_tech_list = (group_user_names['meraki_tech'])
    merakiAList = []
    merakiRList = []
    merakiTList = []
    ###READS ADMIN
    with open(meraki_admin_list_file_new, 'w') as merakiFile:
        merakiFile.write("Names\n")
        for x in range(len(meraki_admin_list)):
            merakiFile.write(f'{meraki_admin_list[x]}\n')
    with open(meraki_admin_list_file, 'r')as old, open (meraki_admin_list_file_new, 'r') as new:
        merOne = old.readlines()
        merTwo = new.readlines()
    with open(meraki_admin_list_file, 'a') as one:
        for line in merTwo:
            if line not in  merOne:
                one.write(line)
                print(f'New data adding "{line.strip()}"')
                merakiAList.append(line.strip())
    os.remove(meraki_admin_list_file_new)
    ###READ ONLY
    with open(meraki_read_list_file_new, 'w') as merakiFile:
        merakiFile.write("Names\n")
        for x in range(len(meraki_read_list)):
            merakiFile.write(f'{meraki_read_list[x]}\n')
    with open(meraki_read_list_file, 'r')as old, open (meraki_read_list_file_new, 'r') as new:
        merOne = old.readlines()
        merTwo = new.readlines()
    with open(meraki_read_list_file, 'a') as one:
        for line in merTwo:
            if line not in  merOne:
                one.write(line)
                print(f'New data adding "{line.strip()}"')
                merakiRList.append(line.strip())
    os.remove(meraki_read_list_file_new)            
    ###READS techs
    with open(meraki_tech_list_file_new, 'w') as merakiFile:
        merakiFile.write("Names\n")
        for x in range(len(meraki_tech_list)):
            merakiFile.write(f'{meraki_tech_list[x]}\n')
    with open(meraki_tech_list_file, 'r')as old, open (meraki_tech_list_file_new, 'r') as new:
        merOne = old.readlines()
        merTwo = new.readlines()
    with open(meraki_tech_list_file, 'a') as one:
        for line in merTwo:
            if line not in  merOne:
                one.write(line)
                print(f'New data adding "{line.strip()}"')
                merakiTList.append(line.strip())
    os.remove(meraki_tech_list_file_new)
    print("Meraki groups read")
    return {'merakiAList' : merakiAList,
            'merakiRList' : merakiRList,
            'merakiTList': merakiTList}

    

    
def main():
    # Run PowerShell commands to retrieve AD group members and save them to CSV files
    run_powershell_command(f'Get-ADGroupMember -Identity SSLVPN-users | Select-Object name | Out-File "{sslvpn_users_file}" -Encoding "utf8"')
    run_powershell_command(f'Get-ADGroupMember -Identity SO_ASA| Select GivenName, SAMAccountName | Out-File "{so_asa_file}" -Encoding "utf8"')
    run_powershell_command(f'Get-ADGroupMember -Identity RADIUS-CiscoDevices| Select GivenName, SAMAccountName | Out-File "{cisco_file}" -Encoding "utf8"')

    # Print current timestamp
    print(f"Script executed at: {datetime.datetime.now()}")
#main()
ciscoResult = cisco_csv_reader()
ciscoList = ciscoResult['ciscoList']
result = asa_csv_reader()
soList = result['soList']
sslList = result['sslList']
merakiResult = meraki_csv_reader()
merakiAList = merakiResult['merakiAList']
merakiRList = merakiResult['merakiRList']
merakiTList = merakiResult['merakiTList']
send_notification_email(soList, sslList, ciscoList, merakiAList, merakiRList, merakiTList)
