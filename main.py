import json
from providers import mdes_token_connect_provider

# Encrypt data
with open('request_examples/request1-data.json') as request_data_file:
    payload = json.load(request_data_file)

# Send request using MC Api core
response = mdes_token_connect_provider.push_accounts(payload)
print(response.get(''))