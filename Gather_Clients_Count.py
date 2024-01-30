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

organization_id = '445912'
networks = dashboard.organizations.getOrganizationNetworks(organization_id)
staff_client_count = 0
wireless_client_count = 0
iot_client_count = 0
guest_client_count = 0



for network in networks:
    network_id = network['id']
    res = requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids", headers=headers)
    if res.status_code == 200:
        ssids = res.json()
        for ssid in ssids:
            if ssid['name'] == "CSV Wireless":
                wireless = ssid['number']
            elif ssid['name'] == "CSV Guest":
                guest = ssid['number']
            elif ssid['name'] == "CSV IOT":
                iot = ssid['number']
    response =  requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/clientCountHistory?ssid=14&resolution=300&autoResolution=True", headers=headers)
    if response.status_code == 200:
        infos = response.json()
        info = infos[-1]
        site_count = 0
        if info['clientCount'] != None:
            staff_client_count += info['clientCount']
            site_count += info['clientCount']
        else:
            pass
        print(f"{site_count} Total Clients on CSV Staff at {network['name']}")
    else:
        pass
    response_wireless =  requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/clientCountHistory?ssid={wireless}&resolution=300&autoResolution=True", headers=headers)
    if response_wireless.status_code == 200:
        data_wireless_infos = response_wireless.json()
        wireless_infos = data_wireless_infos[-1]
        site_count = 0
        if wireless_infos['clientCount'] != None:
            wireless_client_count += wireless_infos['clientCount']
            site_count += wireless_infos['clientCount']
        else:
            pass
        print(f"{site_count} Total Clients on CSV Wireless at {network['name']}")
    else:
        pass
    response_iot =  requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/clientCountHistory?ssid={iot}&resolution=300&autoResolution=True", headers=headers)
    if response_iot.status_code == 200:
        data_iot_infos = response_iot.json()
        iot_infos = data_iot_infos[-1]
        site_count = 0
        if iot_infos['clientCount'] != None:
            iot_client_count += iot_infos['clientCount']
            site_count += iot_infos['clientCount']
        else:
            pass
        print(f"{site_count} Total Clients on CSV IOT at {network['name']}")
    else:
        pass
    response_guest =  requests.get(f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/clientCountHistory?ssid={guest}&resolution=300&autoResolution=True", headers=headers)
    if response_guest.status_code == 200:
        data_guest_infos = response_guest.json()
        guest_infos = data_guest_infos[-1]
        site_count = 0
        if guest_infos['clientCount'] != None:
            guest_client_count += guest_infos['clientCount']
            site_count += guest_infos['clientCount']
        else:
            pass
        print(f"{site_count} Total Clients on CSV Guest at {network['name']}")
    else:
        pass
print(f"CSV Staff Final Count: {staff_client_count}")
print(f"CSV Wireless Final Count: {wireless_client_count}")
print(f"CSV IOT Final Count: {iot_client_count}")
print(f"CSV Guest Final Count: {guest_client_count}")
