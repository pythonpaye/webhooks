from flask import Flask, request
import json
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()  # Get the incoming JSON data
    print(f"Received request body: {json.dumps(data)}")  # Log the payload
    return "Received data successfully", 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))  # Default to 8080 if not specified
    app.run(debug=False, host='0.0.0.0', port=port)