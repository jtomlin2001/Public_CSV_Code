import requests

get_token_url = 'https://app.ninjarmm.com/ws/oauth/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}
token_payload = {
    'grant_type': 'client_credentials',

    'scope': 'monitoring',
    'code': '',
    'refresh_token': '',
    'redirect_uri': 'http://localhost',
    'code_verifier': ''
}

response = requests.post(get_token_url, data=token_payload)
if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f'Access Token: {access_token}')
else:
    print(f'Error: {response.status_code}')

url = 'https://app.ninjarmm.com/v2/organizations'
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+ access_token,
}
total_devices = 0
response = requests.get(url, headers=headers)


orgs = (response.json())

for org in orgs:
    response1 = requests.get(f"https://app.ninjarmm.com/v2/organization/{(org['id'])}/devices/", headers=headers)
    devices = (response1.json())
    for device in devices:
        response2 = requests.get(f"https://app.ninjarmm.com/v2/device/{device['id']}/last-logged-on-user", headers=headers)
        if response2.status_code == 200:
            user = response2.json()
            if user['userName'] == "CSV-DOM\so_millera" or user['userName'] == "CSV-DOM\millera":
                print(user['userName'])
                print(device['systemName'])