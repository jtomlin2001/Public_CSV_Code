import subprocess
import webbrowser
import datetime
import time
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import requests
import json 
from time import sleep
import threading
import os
import asyncio
def get_token():
    graph_api_url = 'https://graph.microsoft.com/v1.0/groups'

    auth_url = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize'
    token_url = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token'
    graph_api_url = 'https://graph.microsoft.com/v1.0/users/tomlinj@clinicasierravista.org/presence'
    refresh_id = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJkYWUxZjk4Yy0xMzRlLTRmMTgtYmE3Ni1iYmU4MjIzZGEyNjEiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vMzcwZmI3ZWUtZTViMC00YmY1LWI5MWItM2I2N2ZlNDI5YTI3L3YyLjAiLCJpYXQiOjE2OTY4NzA5NzAsIm5iZiI6MTY5Njg3MDk3MCwiZXhwIjoxNjk2ODc0ODcwLCJyaCI6IjAuQVJ3QTdyY1BON0RsOVV1NUd6dG5fa0thSjR6NTRkcE9FeGhQdW5hNzZDSTlvbUhPQURrLiIsInN1YiI6Im1XeHRpYXYtM2pxZUMxOE1Ubzh1U2VUYW9qRHJPbVFkY2JONnU2RkRqVDgiLCJ0aWQiOiIzNzBmYjdlZS1lNWIwLTRiZjUtYjkxYi0zYjY3ZmU0MjlhMjciLCJ1dGkiOiJWaWJjd1loM19rMlNQSkRlYjJkZkFBIiwidmVyIjoiMi4wIn0.X6am0M0fCzb5jW5Vjg-FZJWvMKKP2SwoUgwAeNs4wYjfLEHxOVAm8tVCy_JJzwuFaEb7HvtFKjtMv9LCURGRwuMnGPb0HK2m8vRGTFNHb4UvTV0xlvu8CAtOq2mm3rBHL4Xf93p5eBbwgxDg7rCHgf6Cf1pReGLhdeA5zbPe1qL-z-L2Q_bVzWrdaEXZGZArlvoBucOI-t2TINzCFPywPE1mNsVjr5bHkf-9_ily-u4TsTtVjdP_JnkQ_8VEOwIGOE0wn0XSKuX78ayWPsTgLL66NIwcCrNuYvrA3EfpIuu5ZHLt81mk8zWgSmNH3cY5KMn5dQshsPA7U60Rpb3UNA'
    with open('refresh.txt', 'r') as refresh:
        refresh_token = refresh.read()
    refresh_payload = {
        'client_id':client_id,
        'client_secret':client_secret,
        'refresh_token':refresh_token,
        'redirect_uri':"https://localhost",
        'grant_type':"refresh_token",
        'scope':'openid offline_access'
    }
    refresh = requests.post(token_url,data=refresh_payload)
    refresh_info = (refresh.json())
    refresh_token = (refresh_info['refresh_token'])
    access_token = (refresh_info['access_token'])
    with open('access.txt', 'w') as env_file:
        env_file.write(f'{access_token}')
    with open('refresh.txt','w') as refreshtxt:
        refreshtxt.write(f'{refresh_token}')
def get_webex_token():
    token_url = 'https://webexapis.com/v1/access_token'

    with open('webex_refresh.txt', 'r') as refresh:
        refresh_token = refresh.read()
    refresh_payload = {
        'client_id':client_id,
        'client_secret':client_secret,
        'refresh_token':refresh_token,
        'grant_type':"refresh_token", 
    }
    refresh = requests.post(token_url,data=refresh_payload)
    refresh_info = (refresh.json())
    refresh_token = (refresh_info['refresh_token'])
    access_token = (refresh_info['access_token'])
    with open('webex_access.txt', 'w') as env_file:
        env_file.write(f'{access_token}')
    with open('webex_refresh.txt','w') as refreshtxt:
        refreshtxt.write(f'{refresh_token}')
get_token()
get_webex_token()
