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
    print(f"{network['name']}:        {staff_site_count}-{wireless_site_count}-{iot_site_count}-{guest_site_count}")
print(f"CSV Staff Final Count: {staff_client_count}")
print(f"CSV Wireless Final Count: {wireless_client_count}")
print(f"CSV IOT Final Count: {iot_client_count}")
print(f"CSV Guest Final Count: {guest_client_count}")
