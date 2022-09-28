# MDES Token Connect sample integration

## Mastercard documentation
- About tokenization: https://developer.mastercard.com/src-issuers/documentation/issuers/
- About MDES token connect: https://developer.mastercard.com/mdes-token-connect/documentation/
- About push provisioning: https://developer.mastercard.com/src-issuers/documentation/issuers/how_it_works_pushprovision/
- Api reference: https://developer.mastercard.com/mdes-token-connect/documentation/api-reference/api-reference/
- Payload data encryption
https://developer.mastercard.com/platform/documentation/security-and-authentication/securing-sensitive-data-using-payload-encryption/#client-libraries

## Encryption
### Certificate files
- For OAuth1 encryption, `resources/MDES_Token_Connect-sandbox.p12` file is used. 
- For payload data encryption, `token-connect-request-encryption-sandbox.cer` certificate file is used.
### Credentials
```
MDES_TOKEN_CONNECT_CREDENTIALS = {
    "consumer_key": "jupJREh5fcPFzK8KVxYRf7nF3Jr8T9ONP5U7rcRDb17f5c90!790460cb74da40548d041d2e83a6b2b30000000000000000",
    "key_store_path": "resources/MDES_Token_Connect-sandbox.p12",
    "key_alias": "keyalias",
    "key_password": "keystorepassword",
}
```

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
