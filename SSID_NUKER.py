import meraki
import requests
import json

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
time = 0
test = 0
 
ssid_get = requests.get(f"https://api.meraki.com/api/v1/networks/L_672725194338474207/wireless/ssids/0", headers=headers)
if ssid_get.status_code == 200:
    ssid_info = ssid_get.json()
    ssid_info['enabled'] = False
    ssid_info['dot11w'] = {}
    ssid_info['dot11r'] = {}
    ssid_info['activeDirectory'] ={}
    ssid_info['speedBurst'] = {}
    ssid_put = requests.put(f"https://api.meraki.com/api/v1/networks/L_672725194338474207/wireless/ssids/0", headers=headers, data=ssid_info)
    if ssid_put.status_code == 200:
        print(ssid_put.text)
    else: 
        print(ssid_put.text)
