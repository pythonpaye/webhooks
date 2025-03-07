from flask import Flask, request
import json
import os
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()  # Get the incoming JSON data
    print(f"Received request body: {json.dumps(data)}")  # Log the payload

    # Extract the phone number from the incoming data
    phone_info = data.get('Phone', {})
    phone_number = phone_info.get('value')

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
            'phone_number': phone_number
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

    return "Processed request", 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))  # Default to port 8080 if not specified
    app.run(debug=False, host='0.0.0.0', port=port)
