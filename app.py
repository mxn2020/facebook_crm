from bson import ObjectId
import os
from flask import Flask, request, jsonify, jsonify
import requests
from tinydb import TinyDB, Query
from dotenv import load_dotenv
from json import JSONEncoder as FlaskJSONEncoder

from db_connector import get_database_client


class CustomJSONEncoder(FlaskJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)
    
    
app = Flask(__name__)
db = get_database_client()
app.json_encoder = CustomJSONEncoder

load_dotenv()

# Use environment variables
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
APP_SECRET = os.getenv('APP_SECRET')
APP_ID = os.getenv('APP_ID')
FORM_ID = os.getenv('FORM_ID')
PAGE_ID = os.getenv('PAGE_ID')


    
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("Webhook called")
    if request.method == 'GET':
        # Facebook webhook verification (same as before)
        print ("GET request")
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return 'Verification failed', 403
    else:
        # Handle webhook events
        print ("POST request")
        data = request.json
        print(data)  # For debugging
        # Save incoming JSON object details to the database
        db.insert({'leads': data})
                         
        return 'Success', 200
    
@app.route('/webhook_lead_calls', methods=['GET', 'POST'])
def webhook_lead_calls():
    print("Webhook called")
    if request.method == 'GET':
        # Facebook webhook verification (same as before)
        print ("GET request")
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return 'Verification failed', 403
    else:
        # Handle webhook events
        print ("POST request")
        data = request.json
        print(data)  # For debugging
        # Save incoming JSON object details to the database
        db.insert({'lead_calls': data})
        
        # Extract leadgen_id from the webhook data
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'leadgen':
                    leadgen_id = change['value']['leadgen_id']
                    # Fetch lead details using the Graph API
                    lead_details = get_lead_details(leadgen_id, PAGE_ACCESS_TOKEN)
                    if lead_details:
                        # Save the fetched lead details under "leads" key
                        db.insert({'leads': lead_details})
                    
        return 'Success', 200

def get_lead_details(lead_id, access_token):
    """Fetch lead details from the Facebook Graph API."""
    url = f"https://graph.facebook.com/v19.0/{lead_id}?access_token={access_token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch lead details: {response.text}")
        return None

@app.route('/items', methods=['GET'])
def get_items():
    items = db.find_all()
    # Convert ObjectId to str for each item
    print ("items: ", items)
    db_name = db.name
    print ("db_name: ", db_name)
    items = [{**item, '_id': str(item['_id'])} for item in items]
    return jsonify(items), 200

@app.route('/retrieve-leads', methods=['GET'])
def retrieve_leads():
    url = f'https://graph.facebook.com/v12.0/{FORM_ID}/leads?access_token={PAGE_ACCESS_TOKEN}'
    response = requests.get(url)
    if response.status_code == 200:
        leads = response.json()['data']
        for lead in leads:
            db.insert({'retrieve-leads':lead})
        return jsonify(leads), 200
    else:
        return 'Failed to retrieve leads', 500

def get_form_ids(page_id, access_token):
    url = f'https://graph.facebook.com/v12.0/{page_id}/leadgen_forms?access_token={PAGE_ACCESS_TOKEN}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forms = data.get('data', [])
        form_ids = [form['id'] for form in forms]
        print("Form IDs:", form_ids)
        return form_ids
    else:
        print(f"Failed to retrieve forms: {response.text}")
        return []

@app.route('/get-form-ids')
def show_form_ids():
    form_ids = get_form_ids(PAGE_ID, PAGE_ACCESS_TOKEN)
    if form_ids:
        return jsonify({"success": True, "form_ids": form_ids})
    else:
        return jsonify({"success": False, "message": "Could not retrieve form IDs."}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5055))  # Default to 5000 if PORT not in environment
    app.run(debug=False, host='0.0.0.0', port=port)
