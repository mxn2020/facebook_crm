import requests

# Replace this URL with the actual URL of your Flask app's webhook endpoint
webhook_url = 'http://localhost:5055/webhook'

# Test JSON object
test_data = {
    'entry': [{
        'id': '0',
        'time': 1707518948,
        'changes': [{
            'field': 'leadgen',
            'value': {
                'ad_id': '55555555',
                'form_id': '55555555444',
                'leadgen_id': '55555555444',
                'created_time': 1707518948,
                'page_id': '55555555444',
                'adgroup_id': '5555555544'
            }
        }]
    }],
    'object': 'page'
}

# Make a POST request to the webhook endpoint
response = requests.post(webhook_url, json=test_data)

# Print the response from the server
print(f'Status Code: {response.status_code}')
print(f'Response Body: {response.text}')
