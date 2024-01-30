import requests
import json
## Info used to create request and initializing variables
headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
location_list = []
##########################################  POST INFORMATION #########################################################################
payload = {
    "type": "holidays",
    "name": "2024 Holiday Schedule",
    "events": [{
            "name": "New Years",
            "startDate": "2024-01-01",
            "endDate": "2024-01-01",
            "allDayEnabled": True
    },
    {
         "name": "Dr. Martin Luther King",
            "startDate": "2024-01-15",
            "endDate": "2024-01-15",
            "allDayEnabled": True
    },
    {
            "name": "Cesar Chavez",
            "startDate": "2024-04-01",
            "endDate": "2024-04-01",
            "allDayEnabled": True
    },
    {
         "name": "Memorial Day",
            "startDate": "2024-05-27",
            "endDate": "2024-05-27",
            "allDayEnabled": True
    },
    {
            "name": "Independence Day",
            "startDate": "2024-07-04",
            "endDate": "2024-07-04",
            "allDayEnabled": True
    },
        {
            "name": "Labor Day",
            "startDate": "2024-09-02",
            "endDate": "2024-09-02",
            "allDayEnabled": True
    },
    {
         "name": "Thanksgiving Day",
            "startDate": "2024-11-28",
            "endDate": "2024-11-28",
            "allDayEnabled": True
    },
    {
            "name": "Day After Thanksgiving",
            "startDate": "2024-11-29",
            "endDate": "2024-11-29",
            "allDayEnabled": True
    },
    {
            "name": "Christmas Eve",
            "startDate": "2024-12-24",
            "endDate": "2024-12-24",
            "allDayEnabled": True
    },
    {
         "name": "Christmas Day",
            "startDate": "2024-12-25",
            "endDate": "2024-12-25",
            "allDayEnabled": True
    }]
}
########################################## POST INFORMATION #########################################################################
payload = json.dumps(payload)
## Request to get Org ID
org = requests.get("https://webexapis.com/v1/organizations", headers=headers)
## Processing information from request into just the ID
org_info = org.json()
org_items = org_info['items']
org = (org_items[0])
org_id = org['id']
## Get locations and create a list 
locations = requests.get("https://webexapis.com/v1/locations", headers=headers)
locations = locations.json()
## Loop through items in json and extract ID 
for location in locations['items']:
    location_list.append(location['id'])
## Loop through list we just created and run a post with our payload to add schedules
for site in location_list:
    id = site
    schedules = requests.post(f"https://webexapis.com/v1/telephony/config/locations/{id}/schedules", headers=headers, data=payload)
    ##### Use this line to help troubleshooting it will print out errors to the terminal  
    print(schedules.text)
    
