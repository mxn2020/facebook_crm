from flask import Flask, request, jsonify
import requests
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')

VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'  # Replace with your verify token
PAGE_ACCESS_TOKEN = 'YOUR_PAGE_ACCESS_TOKEN'  # Replace with your page access token
FORM_ID = 'YOUR_FORM_ID'  # Replace with your form ID

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("WEBHOOK_VERIFIED")
                return challenge, 200
            else:
                return 'Verification failed', 403
    else:
        data = request.json
        print(data)  # Log webhook data for debugging
        # Process the webhook data as needed
        return 'EVENT_RECEIVED', 200

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
    app.run(debug=True)
