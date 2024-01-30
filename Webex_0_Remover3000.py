import requests

# API endpoint for updating a phone
API_ENDPOINT = f"https://webexapis.com/v1/telephony/config/numbers?locationId={locId}"

# Your client credentials for OAuth 2.0


headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

def update_extension(phone_number, new_extension, id):
    endpoint = f"https://webexapis.com/v1/people/{id}"
    data = {
        "extension": new_extension
    }
    response = requests.put(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Extension for phone number {phone_number} updated successfully")
    else:
        print(f"Failed to update extension for phone number {phone_number}")


def phone_number_cruncher():
    leftList = 0
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    response = requests.get(API_ENDPOINT, headers=headers)
    phone_details = response.json()
    
    if "phoneNumbers" in phone_details:
        for phone in phone_details["phoneNumbers"]:
            phone_number = phone["phoneNumber"]
            extension = phone.get("extension")
            print(f"Phone number: {phone_number}")
            print(f"Extension: {extension}")

                
            owner = phone.get('owner')
            
            if owner and owner.get('id'):
                owner_id = owner['id']
                print(f"Owner ID: {owner_id}")
                endpoint = f"https://webexapis.com/v1/people/{owner_id}"
                
                if extension and len(extension) > 4 and extension.startswith("0"):
                    leftList+=1
                    new_extension = extension[1:5]  
                    print(f"New Extension: {new_extension}")
                    data = {
                    "extension": new_extension
                }
                    response1 = requests.get(endpoint, headers=headers, json=data)
                    print(response1.status_code)
                    print(response1.content)
                    if response1.status_code == 200:
                        print(f"Extension for phone number {phone_number} updated successfully")
                    else:
                        print(f"Failed to update extension for phone number {phone_number}")
            else:
                print("Skipping phone number with no owner ID")
            print(leftList)


# Usage
phone_number_cruncher()



