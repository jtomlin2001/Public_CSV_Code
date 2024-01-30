from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import json
import requests
import os
import csv
print("Site?")
userSite = input()

headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

response = requests.get("https://webexapis.com/v1/locations/", headers=headers)
print(response.status_code)
siteList = response.json()
for sites in siteList['items']:
    if userSite in (sites['name']):
        locId = sites['id'] 
response = requests.get(f"https://webexapis.com/v1/telephony/config/numbers?locationId={locId}", headers=headers)
phone_details = response.json()
if response.status_code == 200:
    for phone in phone_details["phoneNumbers"]:
        phone_number = phone.get("phoneNumber")
        extension = phone.get("extension")
        print(f"Extension: {extension}")  
        owner = phone.get('owner')
        if owner and owner.get('id'):
            owner_id = owner['id']
            print(f"Owner ID: {owner_id}")
            if extension and len(extension) > 4 and extension.startswith("0"):
                new_extension = extension[1:5]  
                print(f"New Extension: {new_extension}")
                data = {
                "extension": new_extension
            }
                response = requests.get(f"https://webexapis.com/v1/people/{owner_id}", headers=headers)
                data = (response.content)
                data = json.loads(data)
                data.update(
    {"extension": new_extension
            })
                response1 = requests.put(f"https://webexapis.com/v1/people/{owner_id}?callingData=true", headers=headers, json=data)
                if response1.status_code == 200:
                    print(f"Extension for phone number {phone_number} updated successfully")
                else:
                    print(f"Failed to update extension for phone number {phone_number}")
        else:
            print("Skipping phone number with no owner ID")
        
siteCsvPath = r"C:\Users\so_tomlinj\Downloads"
dir_list = os.listdir(siteCsvPath)
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()),options = options.add_experimental_option("detach", True))
driver.get('https://admin.webex.com')
print("Connecting to Webex... This process may take up to 30 Seconds")
driver.maximize_window()

# Wait for the page to load
driver.implicitly_wait(10)
# Find the element using XPath and click on it
email = driver.find_element(By.XPATH,'//*[@id="md-input-0"]')
email.click()
email.send_keys("tomlinj@clinicasierravista.org")
signin = driver.find_element(By.XPATH,'/html/body/webex-host-bootstrap/ng-component/webex-auth-feature-layout/main/form/button/span')
signin.click()
microEmail = driver.find_element(By.ID,'i0116')
microEmail.click()
microEmail.send_keys("tomlinj@clinicasierravista.org")
sendEmail = driver.find_element(By.ID, 'idSIButton9')
sendEmail.click()
sleep(2)
passField = driver.find_element(By.ID, 'i0118')
passField.click()
passEnter = driver.find_element(By.ID, "idSIButton9")
passEnter.click()
sleep(4)
print("Connected to Webex!")
passCom = driver.find_element(By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input')
passCom.click()
#sleep(4)
#driver.get("https://admin.webex.com/locations")
#siteSear = driver.find_element(By.XPATH, "/html/body/webex-host-bootstrap/webex-main/div/main/ng-component/webex-page-layout/section/div/main/ng-component/mch-collection/header/div/mch-collection-header/mch-collection-header-left/webex-locations-list-search/md-input-container/div/input")
#siteSear.click()
#sleep(2)
#siteSear.send_keys(userSite)
#webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
#sleep(2)
#firstSite = driver.find_element(By.XPATH, "/html/body/webex-host-bootstrap/webex-main/div/main/ng-component/webex-page-layout/section/div/main/ng-component/mch-collection/section/p-table/div/div[1]/div/cdk-virtual-scroll-viewport/div[1]/table/tbody/tr/td[1]")
#firstSite.click()
#locId = driver.find_element(By.XPATH,"/html/body/webex-host-bootstrap/webex-main/div/main/ng-component/mch-details-page/header/mch-navigation-header/header/mch-details-page-header/section[1]/div/mch-attributes[1]/mch-attribute/span")
#locId = locId.text
#driver.get(f"https://admin.webex.com/manage-users/users?locations={locId}")
sleep(12)
print("Finding Site...")
workspaces = driver.find_element(By.XPATH, '/html/body/webex-host-bootstrap/webex-main/div/nav/webex-sidebar/mch-sidenav-container/mch-sidenav/div/mch-sidenav-group[3]/ul/li[4]/span')
workspaces.click()
filters = driver.find_element(By.XPATH, "/html/body/webex-host-bootstrap/webex-main/div/main/webex-places-list/webex-page-layout/section/header/webex-page-sub-header/div/webex-page-sub-header-left/webex-place-location-multi-selector/md-select/button")
filters.click()
filterSite= driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div[2]/md-input-container/div/input")
filterSite.click()
sleep(1)
filterSite.send_keys(userSite)
site = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div[4]/md-select-item/div/div/div/md-checkbox/label")
site.click()
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
print("Site Found!")
try:
    allBox = driver.find_element(By.XPATH,"/html/body/webex-host-bootstrap/webex-main/div/main/webex-places-list/webex-page-layout/section/div/mch-collection/section/p-table/div/div[1]/div/div[1]/div/table/thead/tr/th[1]/md-checkbox/label")
    allBox.click()
    exportButton = driver.find_element(By.XPATH,'/html/body/webex-host-bootstrap/webex-main/div/main/webex-places-list/webex-page-layout/section/div/mch-collection/header/div/div/mch-bulk-actions-bar/div[2]/div[2]/button/span/span')
    exportButton.click()
    sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
    sleep(2)
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    sleep(5)
    print("Gathering phone data...")
except:
    print(f"could not find any phones at {userSite}")
dir_list = os.listdir(siteCsvPath)
for x in dir_list:
    if x.startswith('workspaces'):
        os.rename(f"{siteCsvPath}\{x}",f"{siteCsvPath}\{userSite}.csv")
with open(f"{siteCsvPath}\{userSite}.csv", 'r') as one:
    lines = one.readlines()
    phone_count = len(lines)-1
    print(f"Collected phone data! There are {phone_count} phones at {userSite}")
for line in lines:
    if line.startswith("ID"):
        pass
    else:
        phone_count -= 1
        idList = (line.split(","))
        id = idList[0]
        phoneName = idList[1]
        driver.get(f"https://admin.webex.com/workspaces/{id}/calling")
        driver.implicitly_wait(10)
        sleep(10)
        textBox = driver.find_element(By.XPATH, '/html/body/webex-host-bootstrap/webex-main/div/main/webex-place-details-shell/mch-details-page/main/div/webex-place-calling-container/webex-call-overview-number/mch-page-section/div/mch-page-section-panel/mch-page-section-row-panel/webex-call-directory-number/mch-page-section-row/div[2]/div/p-table/div/div/table/tbody/tr/td[3]/p')
        extension = (textBox.text)
        print(f"Connected to {phoneName}")
        if extension and len(extension) > 4 and extension.startswith("0"):
            sleep(20)
            print(f"{phoneName} has bad extension")
            new_extension = extension[1:5]
            extBox = driver.find_element(By.XPATH, '/html/body/webex-host-bootstrap/webex-main/div/main/webex-place-details-shell/mch-details-page/main/div/webex-place-calling-container/webex-call-overview-number/mch-page-section/div/mch-page-section-panel/mch-page-section-row-panel/webex-call-directory-number/mch-page-section-row/div[2]/div/p-table/div/div/table/tbody/tr/td[3]/p')
            driver.implicitly_wait(10)
            extBox.click()
            extEdit = driver.find_element(By.XPATH, '/html/body/webex-host-bootstrap/webex-main/div/main/webex-place-details-shell/mch-details-page/main/div/webex-calling-advanced-features-wrapper/webex-call-directory-number-overview/webex-call-directory-number-details/mch-page-section/div/mch-page-section-panel/mch-page-section-row-panel/mch-page-section-row/div[2]/div/form/mch-page-section-row[2]/div[2]/div/md-input-container/div/input')
            extEdit.click()
            action = webdriver.ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            extEdit.send_keys(new_extension)
            sleep(1)
            save = driver.find_element(By.XPATH,'/html/body/webex-host-bootstrap/webex-main/div/main/webex-place-details-shell/mch-save-cancel-bar/button[2]')
            save.click()
            print("Extension has been changed :D")
            sleep(2)
        else:
            print(f"{phoneName} has a valid extension :D")
os.remove(f"{siteCsvPath}\{userSite}.csv")
print("All Devices reconfiged")
input()