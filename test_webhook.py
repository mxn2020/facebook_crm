import requests

# Replace these variables with your actual values
VERIFY_TOKEN = 'my_secure_verify_token'
LOCAL_WEBHOOK_URL = 'http://localhost:5055/webhook'  # Local Flask app URL
HEROKU_WEBHOOK_URL = 'https://facebook-crm-594e80f34b9a.herokuapp.com/webhook'  # Heroku app URL

# Test on local Flask app
print("Testing on local Flask app:")
verification_params_local = {
    'hub.mode': 'subscribe',
    'hub.verify_token': VERIFY_TOKEN,
    'hub.challenge': 'test_challenge_token'  # You can replace this with any token for testing
}
verification_response_local = requests.get(LOCAL_WEBHOOK_URL, params=verification_params_local)
print("Local Verification Response:")
print(verification_response_local.text)

# Test on Heroku deployed app
print("\nTesting on Heroku deployed app:")
verification_params_heroku = {
    'hub.mode': 'subscribe',
    'hub.verify_token': VERIFY_TOKEN,
    'hub.challenge': 'test_challenge_token'  # You can replace this with any token for testing
}
verification_response_heroku = requests.get(HEROKU_WEBHOOK_URL, params=verification_params_heroku)
print("Heroku Verification Response:")
print(verification_response_heroku.text)
