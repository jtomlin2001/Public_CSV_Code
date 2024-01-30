import paramiko
from netmiko import ConnectHandler
import difflib
import datetime
time_now  = datetime.datetime.now().strftime('%m_%d_%Y_TIME_%H-%M')
username = ''
password = ''
ssh = paramiko.SSHClient()
device = {
    'device_type': 'cisco_ios',
    'ip': '172.16.2.254',
    'username': username,
    'password': password,
    'secret': 'L3tM3!n@CSV'
}
ssh = ConnectHandler(**device)
ssh.enable()
running_config = ssh.send_command('show running-config | begin hostname')
startup_config = ssh.send_command('show startup-config | begin hostname')
config_diff = list(difflib.unified_diff(startup_config.splitlines(), running_config.splitlines(), fromfile='startup-config', tofile='running-config', lineterm=''))
output1 = ssh.send_command("show running-config")
startup_config = ssh.send_command('show startup-config')
save_file = open(r"\\csvfile01\IT\Network\Backups 2023\Core_Stack_Running_Config"+time_now+".txt","w")
save_file1 = open(r"\\csvfile01\IT\Network\Backups 2023\Core_Stack_Startup_Config"+time_now+".txt","w")
save_file.write(output1)
save_file1.write(startup_config)
