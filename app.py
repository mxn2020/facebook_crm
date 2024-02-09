import os
from flask import Flask, request, jsonify
import requests
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')

VERIFY_TOKEN = 'my_secure_verify_token'  # Replace with your verify token
PAGE_ACCESS_TOKEN = 'YOUR_PAGE_ACCESS_TOKEN'  # Replace with your page access token
FORM_ID = 'YOUR_FORM_ID'  # Replace with your form ID

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Facebook webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return challenge, 200  # Respond with the challenge token
            else:
                return 'Verification failed', 403
    else:
        # Handle webhook events
        data = request.json
        print(data)  # Process the webhook data as needed
        return 'Success', 200


@app.route('/retrieve-leads', methods=['GET'])
def retrieve_leads():
    url = f'https://graph.facebook.com/v12.0/{FORM_ID}/leads?access_token={PAGE_ACCESS_TOKEN}'
    response = requests.get(url)
    if response.status_code == 200:
        leads = response.json()['data']
        for lead in leads:
            db.insert(lead)
        return jsonify(leads), 200
    else:
        return 'Failed to retrieve leads', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5055))
    app.run(debug=True, port=port)
