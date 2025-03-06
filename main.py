from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()  # Get the incoming JSON data
    print(f"Received request body: {json.dumps(data)}")  # Log the payload
    return "Received data successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Cloud Run expects the app to listen on port 8080
