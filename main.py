#!python
import json
from providers import mdes_token_connect_provider, enrollment_provider

# Send request using MC Api core
response = mdes_token_connect_provider.push_accounts({
  "requestId": "b2afb3cb-ace2-43ee-bfa1-25468bb0fda8",
  "tokenRequestorId": "50123197928",
  "pushFundingAccounts": {
    "encryptedPayload": {
      "encryptedData": [
        {
          "pushAccountId": "CA-132d72d4fcb2f4136a0532d3093ff1ff",
          "fundingAccountData": {
            "cardAccountData": {
              "accountNumber": "5167721052060919",
              "expiryMonth": "12",
              "expiryYear": "23"
            }
          }
        }
      ]
    }
  },
  "signatureData": {
    "callbackURL": "https://sandbox.src.mastercard.com/provision",
    "completeIssuerAppActivation": False,
    "completeWebsiteActivation": False,
    "accountHolderDataSupplied": False,
    "locale": "cs_CZ"
  }
})
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