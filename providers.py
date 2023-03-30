import json
import uuid
from datetime import datetime

import requests
from client_encryption import field_level_encryption
from client_encryption.field_level_encryption_config import FieldLevelEncryptionConfig
from mastercardapicore import BaseObject, Config, OAuthAuthentication, OperationMetadata, RequestMap, Environment
from requests import Request

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
    "encryptionCertificate": "resources/MDESTokenConnectMTFClientEnc1679433687206.pem"
}
#
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

ENVIRONMENT = 'production_mtf'  # sandbox, production


class OperationConfig(object):
    def __init__(self, resourcePath, action, headerParams, queryParams):
        self.resourcePath = resourcePath
        self.action = action
        self.headerParams = headerParams
        self.queryParams = queryParams

    def getResourcePath(self):
        return self.resourcePath

    def getAction(self):
        return self.action

    def getHeaderParams(self):
        return self.headerParams

    def getQueryParams(self):
        return self.queryParams


class BaseMastercardProvider:
    authentication: OAuthAuthentication

    def __init__(self):
        self.authentication = self.get_authentication()

    def set_config(self):
        Config.setAuthentication(self.authentication)
        Config.setDebug(True)
        Config.setEnvironment(ENVIRONMENT)

    def get_authentication(self) -> OAuthAuthentication:
        raise NotImplementedError


class MdesTokenConnectProvider(BaseMastercardProvider):
    def get_authentication(self) -> OAuthAuthentication:

        return OAuthAuthentication(
            MDES_TOKEN_CONNECT_CREDENTIALS["consumer_key"],
            MDES_TOKEN_CONNECT_CREDENTIALS["key_store_path"],
            MDES_TOKEN_CONNECT_CREDENTIALS["key_alias"],
            MDES_TOKEN_CONNECT_CREDENTIALS["key_password"],
        )

    class PushAccount(BaseObject):
        @classmethod
        def getOperationMetadata(self):
            """Set API host"""
            return OperationMetadata('0.1', Environment.mapping[Config.getEnvironment()][0], jsonNative=True)

        @classmethod
        def getOperationConfig(self, _):
            """ Set endpoint and REST method"""
            if 'mtf' in Config.getEnvironment():
                return OperationConfig("/mdes/mtf/connect/1/0/pushMultipleAccounts", "create", [], [])
            return OperationConfig("/mdes/connect/1/0/pushMultipleAccounts", "create", [], [])

        @classmethod
        def query(cls, criteria):
            return cls.execute("", cls(criteria))

    def push_accounts(self, payload):
        self.set_config()

        # Load encryption config
        with open('config.json') as config_file:
            config_data = json.load(config_file)

        if fingerprint := MDES_TOKEN_CONNECT_CREDENTIALS.get('signing_certificate_fingerprint'):
            config_data['encryptionCertificateFingerprint'] = fingerprint
        config_data["encryptionCertificate"] = MDES_TOKEN_CONNECT_CREDENTIALS['encryptionCertificate']
        config = FieldLevelEncryptionConfig(config_data)

        # Encrypt data
        payload = field_level_encryption.encrypt_payload(payload, config)

        mapObj = RequestMap()
        mapObj.set("requestId", str(uuid.uuid4()))
        mapObj.set('pushFundingAccounts', payload['pushFundingAccounts'])
        mapObj.set('tokenRequestorId', payload['tokenRequestorId'])
        mapObj.set("signatureData", payload['signatureData'])

        response = self.PushAccount.query(mapObj)
        return response

mdes_token_connect_provider = MdesTokenConnectProvider()


class EnrollmentProvider:
    def enroll(  # noqa JG06
        self,
        first_name: str,
        last_name: str,
        email: str,
        country: str,  # in iso8166-alpha2 format e.g. CZ
        phone_prefix: str,
        phone_number: str,
        locale: str,
        enrolment_reference: str,
        src_correlation_id: str,
    ):

        """API reference: https://developer.mastercard.com/push-provisioning-via-enroll-api/documentation/api-
        reference/ Key management: https://developer.mastercard.com/push-provisioning-via-enroll-
        api/documentation/tutorials-and-guides/onboarding/#key-management Error Handling:
        https://developer.mastercard.com/push-provisioning-via-enroll-api/documentation/error-handling/

        x-openapi-clientid:
        https://developer.mastercard.com/click-to-pay/documentation/api-reference/cof/delete-saved-cof/#request-header
        https://developer.mastercard.com/click-to-pay/documentation/api-reference/transaction-credentials/#open-api-specification
        https://developer.mastercard.com/click-to-pay/documentation/onboarding/create-new-project/#6-review-the-oauth-credentials

        Other:
        Authorization header:
        https://developer.mastercard.com/platform/documentation/security-and-authentication/using-oauth-1a-to-access-mastercard-apis/#the-authorization-header
        MDES Token Connect:
        https://developer.mastercard.com/mdes-token-connect/documentation/api-reference/api-reference/#apis
        """

        headers = {
            "x-openapi-clientid": MASTERCARD_CLICK_TO_PAY_ENROLL_API["consumer_key"][:48],
            "Content-Type": "application/json",
        }

        data = {
            "srcClientId": MASTERCARD_CLICK_TO_PAY_ENROLL_API["src_client_id"],
            "srcCorrelationId": src_correlation_id,
            "serviceId": "SRC",
            "consumer": {
                "consumerIdentity": {"identityType": "EMAIL_ADDRESS", "identityValue": email},
                "mobileNumber": {"countryCode": phone_prefix, "phoneNumber": phone_number},
                "countryCode": country,
                "languageCode": locale,
                "firstName": first_name,
                "lastName": last_name,
            },
            "complianceSettings": {
                "privacy": {"latestVersionUri": MASTERCARD_CLICK_TO_PAY_ENROLL_API["privacy_notice_url"]},
                "tnc": {"latestVersionUri": MASTERCARD_CLICK_TO_PAY_ENROLL_API["terms_of_use_url"]},
            },
            "cardSource": "ISSUER",
            "enrolmentReferenceData": {
                "enrolmentReferenceId": enrolment_reference,
                "enrolmentReferenceType": "PUSH_ACCOUNT_RECEIPT",
            },
        }

        auth = OAuthAuthentication(
            MASTERCARD_CLICK_TO_PAY_ENROLL_API["consumer_key"],
            MASTERCARD_CLICK_TO_PAY_ENROLL_API["key_store_path"],
            MASTERCARD_CLICK_TO_PAY_ENROLL_API["key_alias"],
            MASTERCARD_CLICK_TO_PAY_ENROLL_API["key_password"],
        )

        enroll_request = Request()
        enroll_request.method = "POST"
        enroll_request.url = MASTERCARD_CLICK_TO_PAY_ENROLL_API["url"]
        enroll_request.data = json.dumps(data, separators=(",", ":"))
        enroll_request.headers = headers
        enroll_request = auth.signRequest(MASTERCARD_CLICK_TO_PAY_ENROLL_API["url"], enroll_request)

        response = requests.request(
            "POST", enroll_request.url, data=enroll_request.data, headers=enroll_request.headers
        )

        print()
        print("TIMESTAMP:")
        print(f"{datetime.utcnow():%Y-%m-%d %H:%M:%S.%f} UTC")
        print("REQUEST URL:")
        print(response.request.url)
        print("REQUEST METHOD:")
        print(response.request.method)
        print("REQUEST HEADERS:")
        print(json.dumps(dict(response.request.headers), indent=4, sort_keys=True))
        print("REQUEST DATA:")
        print(json.dumps(json.loads(response.request.body), indent=4, sort_keys=True))

        print()

        print()
        print("RESPONSE STATUS CODE:")
        print(response.status_code)
        print("RESPONSE HEADERS:")
        print(json.dumps(dict(response.headers), indent=4, sort_keys=True))

        print("RESPONSE DATA:")
        print(json.dumps(response.json(), indent=4, sort_keys=True))


enrollment_provider = EnrollmentProvider()