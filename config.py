ENVIRONMENT = 'production_mtf'  # sandbox, production

MDES_TOKEN_CONNECT_ENCRYPTION_CONFIG = {
  "paths": {
    "$": {
      "toEncrypt": {
        "pushFundingAccounts.encryptedPayload.encryptedData": "pushFundingAccounts.encryptedPayload"
      },
      "toDecrypt": {}
    }
  },
  "ivFieldName": "iv",
  "encryptedKeyFieldName": "encryptedKey",
  "encryptedValueFieldName": "encryptedData",
  "dataEncoding": "hex",
  "oaepPaddingDigestAlgorithm": "SHA-512",
  "encryptionCertificateFingerprintFieldName": "publicKeyFingerprint",
  "oaepPaddingDigestAlgorithmFieldName": "oaepHashingAlgorithm"
}


#SANDBOX
# MDES_TOKEN_CONNECT_CREDENTIALS = {
#     "consumer_key": "jupJREh5fcPFzK8KVxYRf7nF3Jr8T9ONP5U7rcRDb17f5c90!790460cb74da40548d041d2e83a6b2b30000000000000000",
#     "key_store_path": "resources/MDES_Token_Connect-sandbox.p12",
#     "key_alias": "keyalias",
#     "key_password": "keystorepassword",
#     "encryptionCertificate": "resources/token-connect-request-encryption-sandbox.cer",

# }


#PROD
MDES_TOKEN_CONNECT_CREDENTIALS = {
    "consumer_key": "iPtJJPRTiiYtWC56ecylscshuHUV32eAzmQS-If4765e9383!524ddd117d9f4b8eb284766e70cf96ce0000000000000000",
    "key_store_path": "resources/twisto_mc_connect_prod-production.p12",
    "key_alias": "twisto_mc_connect_prod",
    "key_password": "&rcs03a8d1SB",
    "signing_certificate_fingerprint": "4286bd8eb836908ce0e9a96dea39352355c86a5d5f8b3e732b62621bc470b30d",
    "encryptionCertificate": "resources/MDESTokenConnectMTFClientEnc1679433687206.pem",

}

MASTERCARD_CLICK_TO_PAY_ENROLL_API = {
    "src_client_id": "2971f926-b7e6-4c15-a380-e15f279d115e",
    "url": "https://sandbox.api.mastercard.com/src/api/digital/payments/cards",
    "consumer_key": "S5oZ_-lQglR09W2hGf1uSGbFXl-_9NUiu5sDv3o917474bef!723b50e5d7b9487a9c55bb1aaf4e21b30000000000000000",
    "key_store_path": "resources/mastercard_src_system_sandbox.p12",
    "key_alias": "defaultsandboxsigningkey",
    "key_password": "vWMrKVclmabJjpNdaQWv",
    "privacy_notice_url": "https://www.mastercard.com/global/click-to-pay/country-listing/privacy.html?locale=cs_CZ",
    "terms_of_use_url": "https://www.mastercard.com/global/click-to-pay/country-listing/terms.html?locale=cs_CZ",
    "learn_more_url": "https://www.mastercard.cz/cs-cz/osobni/bezkontaktni-platby/click-to-pay.html",
}