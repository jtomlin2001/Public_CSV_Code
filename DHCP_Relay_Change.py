import meraki
import requests

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
networks = dashboard.organizations.getOrganizationNetworks(organization_id)
time = 0
test = 0

for network in networks:
    network_id = network['id']
    url =  requests.get(f"{base_url}/networks/{network_id}/appliance/vlans", headers={'Authorization': f'Bearer {api_key}'})
    vlan_data = (url.json())

    for vlan in vlan_data:
        try:
            print(str(vlan['dhcpRelayServerIps']))
        except:
            print("test")
        try:
            vlan_id = str({vlan['id']}).replace("{","").replace("}", "")
            print(vlan_id)
            vlan_name = str({vlan['name']}).replace("{","").replace("}", "")
            vlan_dhcp_handling = str({vlan['dhcpHandling']}).replace("{","").replace("}", "")
            vlan_subnet = str({vlan['subnet']}).replace("{","").replace("}", "")
            try:
                vlan_dhcp_relay = (str(vlan['dhcpRelayServerIps']))
                relay_ip = vlan_dhcp_relay.replace("[","").replace("]", "").replace("'","")
            except:
                print()
        except:
            print(f"{network['name']} Has no Vlans")