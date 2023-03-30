# MDES Token Connect sample integration

## Project setup
You need python 3.9 or higher to run this project
You can install requirements using `poetry install` or
```
pip install -r requirements.txt
```

### Config
Config for client ids, file setup etc. can be found in file `config.py`

## Run
the requests are setup and run from `main.py`
to run the request use `./main.py` or `python main.py` from the project root

## Mastercard documentation
- About tokenization: https://developer.mastercard.com/src-issuers/documentation/issuers/
- About MDES token connect: https://developer.mastercard.com/mdes-token-connect/documentation/
- About push provisioning: https://developer.mastercard.com/src-issuers/documentation/issuers/how_it_works_pushprovision/
- Api reference: https://developer.mastercard.com/mdes-token-connect/documentation/api-reference/api-reference/
- Payload data encryption
https://developer.mastercard.com/platform/documentation/security-and-authentication/securing-sensitive-data-using-payload-encryption/#client-libraries

## SDKs
### Python
- payload encryption python sdk: https://github.com/Mastercard/client-encryption-python
- OAuth1 encryption python sdk: mastercard-core-api
### Java
- payload encryption sdk: https://search.maven.org/artifact/com.mastercard.developer/client-encryption
  - github: https://github.com/Mastercard/client-encryption-java
- OAuth1 encryption Java sdk: https://search.maven.org/artifact/com.mastercard.developer/oauth1-signer
  - github: https://github.com/Mastercard/oauth1-signer-java
- 

## URLs
- sandbox: https://sandbox.api.mastercard.com/mdes/connect/1/0/pushMultipleAccounts
- production: https://api.mastercard.com/mdes/connect/1/0/pushMultipleAccounts

## Example request
Example request data, encrypted form, headers and response in JSON can be found in `request_examples` folder
