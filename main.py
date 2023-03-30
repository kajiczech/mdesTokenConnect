import json
from providers import mdes_token_connect_provider, enrollment_provider

# Encrypt data
with open('request_examples/request1-data.json') as request_data_file:
    payload = json.load(request_data_file)

# Send request using MC Api core
response = mdes_token_connect_provider.push_accounts(payload)
response = json.loads(response.get(''))
print(response)

enroll_response = enrollment_provider.enroll(
    first_name="Karel",
    last_name="Cech",
    email="carl.cech@gmail.com",
    country="CZ",
    phone_prefix="420",
    phone_number="777853040",
    locale='cs',
    enrolment_reference=response['pushAccountReceipts'][0]['pushAccountReceipt'],
    src_correlation_id='04ae4379-e531-41ce-6974-d330c5feb819',
)