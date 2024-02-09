import hashlib
import hmac
import requests
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Replace 'YOUR_APP_SECRET' with your actual Facebook App Secret
APP_SECRET = 'YOUR_APP_SECRET'
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'

# Function to validate the request from Facebook
def verify_facebook_signature(request):
    signature = request.headers.get('X-Hub-Signature')
    if not signature:
        return False
    sha1, received_signature = signature.split('=')
    expected_signature = hmac.new(
        key=APP_SECRET.encode(),
        msg=request.get_data(),
        digestmod=hashlib.sha1
    ).hexdigest()
    return hmac.compare_digest(expected_signature, received_signature)

@app.route('/webhook/leads', methods=['GET', 'POST'])
def handle_leads():
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            return challenge
        abort(403)
    else:
        if not verify_facebook_signature(request):
            abort(403)
        # Process the leadgen webhook data
        data = request.json
        print("Leadgen data received:", data)
        # Here you can process the leadgen data
        return 'Webhook received', 200

@app.route('/leads/bulk', methods=['GET'])
def retrieve_bulk_leads():
    page_access_token = 'YOUR_PAGE_ACCESS_TOKEN'
    form_id = 'YOUR_FORM_ID'
    fields = 'id,name,email,phone_number'
    url = f'https://graph.facebook.com/v12.0/{form_id}/leads?access_token={page_access_token}&fields={fields}'

    response = requests.get(url)
    if response.status_code == 200:
        leads = response.json()
        return jsonify(leads)
    else:
        return jsonify({"error": "Failed to retrieve leads"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
