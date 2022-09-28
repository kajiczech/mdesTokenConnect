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

### Unencrypted request
```json
{
  "requestId": "b2afb3cb-ace2-43ee-bfa1-25468bb0fda8",
  "tokenRequestorId": "50123197928",
  "pushFundingAccounts": {
    "encryptedPayload": {
      "encryptedData": [
        {
          "pushAccountId": "CA-132d72d4fcb2f4136a0532d3093ff1ab",
          "fundingAccountData": {
            "cardAccountData": {
              "accountNumber": "5123456789012345",
              "expiryMonth": "12",
              "expiryYear": "23"
            },
            "accountHolderData": {
              "accountHolderName": "John Doe",
              "accountHolderAddress": {
                "line1": "100 1st Street",
                "line2": "Apt. 4B",
                "city": "St. Louis",
                "countrySubdivision": "MO",
                "postalCode": "61000",
                "country": "USA"
              },
              "accountHolderEmailAddress": "john.doe@anymail.com",
              "accountHolderMobilePhoneNumber": {
                "countryDialInCode": "1",
                "phoneNumber": "7181234567"
              }
            }
          }
        }
      ]
    }
  },
  "signatureData": {
    "callbackURL": "https://sandbox.src.mastercard.com/provision",
    "completeIssuerAppActivation": true,
    "completeWebsiteActivation": false,
    "accountHolderDataSupplied": true,
    "locale": "en_US"
  }
}
```

### Headers

```json
{
  "Accept": "application/json; charset=UTF-8",
  "Content-Type": "application/json; charset=UTF-8",
  "User-Agent": "mastercard-api-core(python):1.4.12/0.1",
  "Authorization": "OAuth oauth_consumer_key=\"jupJREh5fcPFzK8KVxYRf7nF3Jr8T9ONP5U7rcRDb17f5c90%21790460cb74da40548d041d2e83a6b2b30000000000000000\",oauth_nonce=\"GOllrXOEvWiVRJAS\",oauth_timestamp=\"1664377843\",oauth_signature_method=\"RSA-SHA256\",oauth_version=\"1.0\",oauth_body_hash=\"c4fBJa7Fh0qJ7PB3Q2M9fQav6RYs8bXkVPfzV8pNWZc%3D\",oauth_signature=\"R7Q6aMZLcnUKLTB3PanyqDTiI%2BjsdF8VnX73YaF8ivmSKI8dbVHTh0Rr%2B9NY10U2m%2BmQ8WJjemumlksDAXe6fu%2BO%2BUr%2BqrkdxEmLIjj7QTdalKdv6S4VeXbH8UahbihRDKYUbENdUrdIt9IepzhDe1s86UwOBpg6fec%2F%2BvEc5tASPYNpzTLjsMD5cnqKBPrO5N9Uyb2TNBpAk%2BY6AwLJmfbSy0NHydUAnPpcbvyQ3Oa3EbgOj6P98eEepVbwxjD967fVs8X5JyglaLQDXSSGUlQpyepWLyI%2BUNafNsN6HxobelZ8v2Gqzse9cPha5hQs%2B3ZuAcpSQBPfARo8y3N4sw%3D%3D\"",
  "Content-Length": "2185"
}
```

### Encrypted Payload
```json
{
  "requestId": "8225ab7b-c6c2-4fdf-99df-520c373dbe23",
  "pushFundingAccounts": {
    "encryptedPayload": {
      "encryptedData": "e2bcb5923b2e55bdd0db317887c557178e0c29fe37fc4ab973caa8cde0fac103d96cfc7762811ae36a9b07b3d9dc99db9cf8a5b2a30361169be0e9211602e8b10ad142b7c3a4de761aa347d159af9f026c51bfc9db031327a17fd6e09bcf4731ea47c500f6c5cae0018686b08cdae4baef34f2100910bd20ec01a8a4b31f68d0dab75c83ccc6b78f4358ad9bfa7741294c9e652935469e1153d37c5832517a6351de848dc065468a732c688407c23d9fcb3ef268396deb6312f014223fa957b80ae68d866e13c45a52227e31b19972c3f82c3deb57ad93a76f8acfb485a50c1c40182751e4da2729830f2ed2523407e07cfd7ab99af1ef15d86c0de5ea3c93f7dcb4bc71b83e1abb35f8f0334ba0c9044b62874fc62994369bd36ddbad76d042d9c235d311be86654ecd06258aae410ad22dd2a76682fff38f5c6abcf5e7d2bfed7ade6ad0fcfcbf10664be98569a5bb7b644c029913ef4885288c289872d831f5be5b58221d3983ce42f82962e6886367f65eaf9b0cef893dc949c714d405cae21aba971de86e323504ededf584c3e0bb04f0580ed6455d47edaa170ec002c11bb78484db92e7db471cc4bd79937a3cc0563bd61e0eb59f30438cbf6fbaf419ad6c39c009a053d5710bec6b8450bdeb2e38605c5a8a01a783134cfd0afffb8ebb5cf0d0e64be28747787816bac30b5870e04d7e14ec6a7ea11ada3eac1e3e47db40195205f40981aef2f3fc2608b80c31a57b7f792ae9e4c3f9f0ecb4edee94678622d1ec1abc83378926fc632f5599",
      "encryptedKey": "141f0a813b744235edf9ef67c9c5afc8cab4798165628b9bcda3de72f9ae218ce016378b60d35b92c48dc2fcc31d6e57fdf7aeb755419ae6e590cba0b74d895b38c4a777800a617453b66a0c3a33df78c75c48999e5c5660743ad61bcad6f7f8d7f5f57a01f181afbe8eb784ec4125bd1a483628df82fa7eae97a15891b4f77e654f9b5320ce32d536e67559e686cb47f841715cc78ee08e1eda0ec8675ebce81031d6a86de00117586e5d84f4e8bec051d54f101152b8b240536ccf43c4214427f7e0f2b9de6180a7dc2aaf3b11c763b2bdf59eb279f208d69c75353c96e12331adb7236e5af44f8752df92686aa3c56901dc856a8ab76a382f4aa67dcd14aa",
      "iv": "d06ac8d99c35109bb4cb4be2428f25eb",
      "oaepHashingAlgorithm": "SHA512",
      "publicKeyFingerprint": "3e3ff1c50fd4046b9a80c39d3d077f7313b92ea01462744bfe50b62769dbef68"
    }
  },
  "tokenRequestorId": "50123197928",
  "signatureData": {
    "callbackURL": "https://sandbox.src.mastercard.com/provision",
    "completeIssuerAppActivation": true,
    "completeWebsiteActivation": false,
    "accountHolderDataSupplied": true,
    "locale": "en_US"
  }
}
```

### Response
```json
{
  "pushAccountReceipts": [
    {
      "pushAccountId": "CA-132d72d4fcb2f4136a0532d3093ff1ab",
      "pushAccountReceipt": "MCC-STL-43233098-64B2-4930-A2D1-3D778894B02B"
    }
  ],
  "availablePushMethods": [
    {
      "type": "WEB",
      "uri": "https://sandbox.src.mastercard.com/provision"
    }
  ],
  "signature": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwOTUyMzE2MTc0MTI5MTU4MDYifQ.eyJwdXNoQWNjb3VudFJlY2VpcHRzIjpbIk1DQy1TVEwtNDMyMzMwOTgtNjRCMi00OTMwLUEyRDEtM0Q3Nzg4OTRCMDJCIl0sImNhbGxiYWNrVVJMIjoiaHR0cHM6Ly9zYW5kYm94LnNyYy5tYXN0ZXJjYXJkLmNvbS9wcm92aXNpb24iLCJjb21wbGV0ZVdlYnNpdGVBY3RpdmF0aW9uIjpmYWxzZSwiYWNjb3VudEhvbGRlckRhdGFTdXBwbGllZCI6dHJ1ZSwibG9jYWxlIjoiZW5fVVMifQ.e-qIRpW_uEy2Ecd2_dhNNudy02o0wfw36PqpHwZUspkSskUsEgrBffyEiHGwCpuwVCKkh4T6YWlb9j5A3O-nUOCIq4CP4FsdViWUrUbSV8WR56YfxHnHV81XAzxu97MHpdfXHtnXwvogGV5hPbgJd9Eip6FctrcJEOCsns2paN8lSwxwBrNQ7ers40c2KPUCSBhqNGEeMOQSngAA129hA7tvwBr-CBEFP-L2dnAPrrkhlY3-aVxl8aohlEoqREhUtw7yVArxvEGOFXKfwCBmwst5iTSbvXpHP_h94OnJTV_rDOPbXCM27DsGeAYe7VECQBFQw79Z2rRmSkPPQ-9oWA",
  "tokenRequestorSignatureSupport": true,
  "responseId": "78de6ce0-df4f-4135-ae33-ff727795165e"
}
```
