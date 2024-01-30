import meraki
import requests

api_key = input("Add API Key Here: ")
ssid_name = input("Name of desired SSID: ")
radius_ip = input("IP Address of Radius Server: ")
Secret = input("Secret for Authentication: ")
quest = int(input("Did you set up 1 or 2 Radius servers? "))
if quest == 1:
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

    response = dashboard.organizations.getOrganizations()
    org_info = response[0]
    organization_id = (org_info['id'])
    networks = dashboard.organizations.getOrganizationNetworks(organization_id)
    time = 0
    test = 0

    payload =  f'''{{
        "name": "{ssid_name}",
        "enabled": true,
        "splashPage": "None",
        "ssidAdminAccessible": false,
        "authMode": "8021x-radius",
        "dot11w": {{
            "enabled": false,
            "required": false
        }},
        "dot11r": {{
            "enabled": false,
            "adaptive": false
        }},
        "encryptionMode": "wpa",
        "wpaEncryptionMode": "WPA2 only",
        "radiusServers": [
            {{
                "host": "{radius_ip}",
                "port": 1812,
                "secret": "{Secret}",
            }},
        ],
        "radiusAccountingEnabled": false,
        "radiusTestingEnabled": true,
        "radiusServerTimeout": 1,
        "radiusServerAttemptsLimit": 3,
        "radiusFallbackEnabled": false,
        "radiusProxyEnabled": false,
        "radiusCoaEnabled": true,
        "radiusCalledStationId": "$NODE_MAC$:$VAP_NAME$",
        "radiusAuthenticationNasId": "$NODE_MAC$:$VAP_NUM$",
        "radiusAttributeForGroupPolicies": "Filter-Id",
        "ipAssignmentMode": "Bridge mode",
        "useVlanTagging": false,
        "radiusOverride": false,
        "minBitrate": 11,
        "bandSelection": "Dual band operation",
        "perClientBandwidthLimitUp": 0,
        "perClientBandwidthLimitDown": 0,
        "perSsidBandwidthLimitUp": 0,
        "perSsidBandwidthLimitDown": 0,
        "mandatoryDhcpEnabled": false,
        "lanIsolationEnabled": false,
        "visible": true,
        "availableOnAllAps": true,
        "availabilityTags": [],
        "speedBurst": {{ "enabled": false }}
    }}'''

    for network in networks:
        network_id = network['id']
        response =  requests.put(f"{base_url}/networks/{network_id}/wireless/ssids/14", headers=headers, data = payload)
        if response.status_code == 200:
            print(f"{network['name']} Successfully added SSID!")
elif quest == 2:
    radius_ip_2 = input("IP Address of 2nd RADIUS Server: ")
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

    response = dashboard.organizations.getOrganizations()
    org_info = response[0]
    organization_id = (org_info['id'])
    networks = dashboard.organizations.getOrganizationNetworks(organization_id)
    time = 0
    test = 0

    payload =  f'''{{
        "name": "{ssid_name}",
        "enabled": true,
        "splashPage": "None",
        "ssidAdminAccessible": false,
        "authMode": "8021x-radius",
        "dot11w": {{
            "enabled": false,
            "required": false
        }},
        "dot11r": {{
            "enabled": false,
            "adaptive": false
        }},
        "encryptionMode": "wpa",
        "wpaEncryptionMode": "WPA2 only",
        "radiusServers": [
            {{
                "host": "{radius_ip}",
                "port": 1812,
                "secret": "{Secret}",
            }},
            {{
                "host": "{radius_ip_2}",
                "port": 1812,
                "secret": "{Secret}",
            }}
        ],
        "radiusAccountingEnabled": false,
        "radiusTestingEnabled": true,
        "radiusServerTimeout": 1,
        "radiusServerAttemptsLimit": 3,
        "radiusFallbackEnabled": false,
        "radiusProxyEnabled": false,
        "radiusCoaEnabled": true,
        "radiusCalledStationId": "$NODE_MAC$:$VAP_NAME$",
        "radiusAuthenticationNasId": "$NODE_MAC$:$VAP_NUM$",
        "radiusAttributeForGroupPolicies": "Filter-Id",
        "ipAssignmentMode": "Bridge mode",
        "useVlanTagging": false,
        "radiusOverride": false,
        "minBitrate": 11,
        "bandSelection": "Dual band operation",
        "perClientBandwidthLimitUp": 0,
        "perClientBandwidthLimitDown": 0,
        "perSsidBandwidthLimitUp": 0,
        "perSsidBandwidthLimitDown": 0,
        "mandatoryDhcpEnabled": false,
        "lanIsolationEnabled": false,
        "visible": true,
        "availableOnAllAps": true,
        "availabilityTags": [],
        "speedBurst": {{ "enabled": false }}
    }}'''

    for network in networks:
        network_id = network['id']
        response =  requests.put(f"{base_url}/networks/{network_id}/wireless/ssids/14", headers=headers, data = payload)
        if response.status_code == 200:
            print(f"{network['name']} Successfully added SSID!")
    
