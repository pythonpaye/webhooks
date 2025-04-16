from flask import Flask, request
import json
import os
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()  # Get the incoming JSON data
    # print(f"Received request body: {json.dumps(data)}")

    # Extract the "Community Checkbox" value
    community_checkbox_info = data.get('Subscribe to our Arizona Cardinals general text line to get real-time game day updates, special offers, and more!', {})
    community_checkbox_value = community_checkbox_info.get('value')

    # Check if the "Community Checkbox" value is '1'
    if community_checkbox_value == ['1']:
        # Extract the data fields from the incoming data
        # Phone Number
        phone_info = data.get('Phone', {})
        phone_number = phone_info.get('value')

        # Name
        given_name_info = data.get('First Name', {})
        given_name = given_name_info.get('value')
        surname_info = data.get('Last Name', {})
        surname = surname_info.get('value')

        # Birthday
        birthday_info = data.get('Date of Birth', {})
        birthday = birthday_info.get('value')
        date_obj = datetime.strptime(birthday, "%b %d, %Y")
        birthday_formatted = date_obj.strftime("%Y-%m-%d")

        # City
        city_info = data.get('City', {})
        city = city_info.get('value')

        if phone_number:
            # Define the API endpoint
            url = f'https://api.community.com/webhooks/v1/community/f1590556-33c9-46ba-a565-16eca1a1ef28/subscription_create'

            # Set up the headers, including the Authorization Bearer token
            headers = {
                'Authorization': f'Bearer community_api_8e69ceb0462a505d255ac06bac0f40c79f09c992',
                'Content-Type': 'application/json'
            }

            # Define the payload data
            payload = {
                'communication_channel': 'sms',
                'phone_number': phone_number,
                'given_name': given_name,
                'surname': surname,
                'date_of_birth': birthday_formatted,
                'city': city
            }

            # Send the POST request
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()  # Raise an error for bad status codes
                print('Successfully sent data to Community API.')
            except requests.exceptions.RequestException as e:
                print(f'Error sending data to Community API: {e}')
        else:
            print('Phone number not found in the request data.')
    else:
        print('Community Checkbox is not checked or not present.')

    return "Processed request", 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))  # Default to port 8080 if not specified
    app.run(debug=False, host='0.0.0.0', port=port)
