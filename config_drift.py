import netmiko
import paramiko
from netmiko import ConnectHandler
import difflib
router_ip = '172.16.2.254'

ssh = paramiko.SSHClient()
device = {
                'device_type': 'cisco_ios',
                'ip': router_ip,
                'username': username,
                'password': password,

            }
ssh = ConnectHandler(**device)
ssh.enable()
running_config = ssh.send_command('show running-config | begin username')
startup_config = ssh.send_command('show startup-config | begin username')
ssh.disconnect()
config_diff = list(difflib.unified_diff(startup_config.splitlines(), running_config.splitlines(), fromfile='startup-config', tofile='running-config', lineterm = ''))
if config_diff == []:
    print("no config drift detected")
else:
    print(config_diff)
