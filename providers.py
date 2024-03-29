import json
import uuid
from datetime import datetime

import requests
from client_encryption import field_level_encryption
from client_encryption.field_level_encryption_config import FieldLevelEncryptionConfig
from mastercardapicore import BaseObject, Config, OAuthAuthentication, OperationMetadata, RequestMap, Environment
from requests import Request

from config import MDES_TOKEN_CONNECT_CREDENTIALS, MASTERCARD_CLICK_TO_PAY_ENROLL_API, ENVIRONMENT, MDES_TOKEN_CONNECT_ENCRYPTION_CONFIG


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
        config_data = MDES_TOKEN_CONNECT_ENCRYPTION_CONFIG
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