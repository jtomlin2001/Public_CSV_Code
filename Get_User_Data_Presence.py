import subprocess
import webbrowser
import datetime
import time
import csv
import os
import smtplib
from tinydb import TinyDB, Query
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import requests
import json 
from time import sleep
import threading
import os
import asyncio
import httpx
import asyncio
import time
from tinydb import TinyDB, Query

db = TinyDB('C:/Users/so_tomlinj/Documents/Coding/db.json')
db1 = TinyDB('C:/Users/so_tomlinj/Documents/Coding/db_webex.json')
starter = time.time()

async def fetch_users(url, headers):
    async with httpx.AsyncClient() as client:
        while url:
            info = await client.get(url, headers=headers)
            info.raise_for_status()
            user_data = info.json()
            for user in user_data['value']:
                db.insert({'Name': user['displayName'], 'id': user['id']})
            url = user_data.get('@odata.nextLink')

async def get_user_list():
    start_time = time.time()
    with open('access.txt', 'r') as access:
        access_token = access.read()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'ConsistencyLevel': 'eventual'
    }

    get_user_url = "https://graph.microsoft.com/v1.0/groups/fe10e5e7-cdb6-43e9-ad31-7a7798ce4532/members"
    fresno_get_user = "https://graph.microsoft.com/v1.0/groups/2748aeb0-f949-48bb-b9db-5006b7ae820f/members"

    await asyncio.gather(
        fetch_users(get_user_url, headers),
        fetch_users(fresno_get_user, headers)
    )

    end_time = time.time()
    print(f"Gathered Users List from Teams, Elapsed Time: {end_time - start_time} Seconds")

async def get_user_presence():
    start_time = time.time()
    graph_api_url = 'https://graph.microsoft.com/v1.0/communications/getPresencesByUserId'
    users_table = db.table('_default')
    user_data = users_table.all()
    User = Query()
    user_ids = [entry['id'] for entry in user_data]
    max_users_per_request = 650
    user_batches = [user_ids[i:i + max_users_per_request] for i in range(0, len(user_ids), max_users_per_request)]

    async def fetch_batch(batch):
        with open('access.txt', 'r') as access:
            access_token = access.read()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        body = {'ids': batch}
        async with httpx.AsyncClient() as client:
            response = await client.post(graph_api_url, headers=headers, json=body)
            if response.status_code == 200:
                batch_data = response.json()
                for user in batch_data['value']:
                    db.update({'availability': user['availability'], 'status': user['activity']}, User.id == f'{user['id']}')
            else:
                print(f"Error: {response.status_code} - {response.text}")

    await asyncio.gather(*(fetch_batch(batch) for batch in user_batches))

    end_time = time.time()
    print(f"Gathered Teams Presences, Elapsed Time: {end_time - start_time} Seconds")

async def update_webex():
    start_time = time.time()
    webex_all_people = 'https://webexapis.com/v1/people?callingData=false&max=1000'
    with open('webex_access.txt', 'r') as access:
        access_token = access.read()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    async def fetch_people():
        person_count = 0
        people_request = await httpx.get(webex_all_people, headers=headers)
        people_request.raise_for_status()
        people = people_request.json()

        for person in people['items']:
            person_count += 1
            User = Query()
            existing_entry = db1.search(User.id == person['id'])

            if existing_entry:
                db1.update({'id': person['id'], 'status': person['status'], "Name": person['displayName']}, Query().id == person['id'])
            else:
                db1.insert({"Name": person['displayName'], 'id': person['id'], 'status': person['status']})

        if 'Link' in people_request.headers and 'rel="next"' in people_request.headers['Link']:
            next_url = people_request.headers['Link'].split(';')[0][1:-1]
            people_request = await httpx.get(next_url, headers=headers)
            people_request.raise_for_status()
            people = people_request.json()

            for person in people['items']:
                person_count += 1
                db1.insert({"Name": person['displayName'], 'id': person['id'], 'status': person['status']})

    await fetch_people()

    end_time = time.time()
    print(f"Gathered Webex Users and Presences, Elapsed Time: {end_time - start_time} Seconds")

async def sync_webex_to_teams():
    start_time = time.time()

    with open('webex_access.txt', 'r') as access:
        access_token = access.read()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    teams_users_table = db.table('_default')
    teams_user_data = teams_users_table.all()
    webex_users_table = db1.table('_default')
    webex_user_data = webex_users_table.all()
    users_to_update = []

    for webex_user in webex_user_data:
        webex_display_name = webex_user['Name']
        teams_user = next((user for user in teams_user_data if user['Name'] == webex_display_name), None)
        if teams_user and webex_display_name == "Chris Smith":
            if teams_user['status'] != webex_user['status']:
                if teams_user['status'] == 'Offline':
                    trans_status = 'pending'
                elif teams_user['status'] == 'PresenceUnknown':
                    trans_status = 'unknown'
                elif teams_user['status'] == 'OffWork':
                    trans_status = 'OutOfOffice'
                elif teams_user['status'] == 'InACall':
                    trans_status = 'call'
                elif teams_user['status'] == 'Available':
                    trans_status = 'active'
                users_to_update.append({'id': webex_user['id'], 'status': trans_status})
                print(users_to_update)

    if users_to_update:
        for user in users_to_update:
            webex_update_url = f'https://webexapis.com/v1/people/{user["id"]}'
            put_data = {
                "status": user["status"]
            }
            #sync with httpx.AsyncClient() as client:
            #   response = await client.put(webex_update_url, headers=headers, json=put_data)
            #   if response.status_code == 200:
            #       print(f"Updated presence for user {user['id']} successfully.")
            #   else:
            #       print(f"Failed to update presence for user {user['id']}. Status code: {response.status_code}")

    end_time = time.time()
    print(f"Synced Teams data to webex, Elapsed Time: {end_time - start_time} Seconds")

# Call the async functions using asyncio
async def main():
    await get_user_list()
    await get_user_presence()
    await update_webex()
    await sync_webex_to_teams()

asyncio.run(main())
ender_time = time.time()
print(f"Total Elapsed Time {ender_time - starter} Seconds")
db1.truncate()
db1.all()