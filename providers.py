import json
import uuid

from client_encryption import field_level_encryption
from client_encryption.field_level_encryption_config import FieldLevelEncryptionConfig
from mastercardapicore import BaseObject, Config, OAuthAuthentication, OperationMetadata, RequestMap, Environment

MDES_TOKEN_CONNECT_CREDENTIALS = {
    "consumer_key": "jupJREh5fcPFzK8KVxYRf7nF3Jr8T9ONP5U7rcRDb17f5c90!790460cb74da40548d041d2e83a6b2b30000000000000000",
    "key_store_path": "resources/MDES_Token_Connect-sandbox.p12",
    "key_alias": "keyalias",
    "key_password": "keystorepassword",
}


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
        Config.setEnvironment("sandbox")

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
            return OperationConfig("/mdes/connect/1/0/pushMultipleAccounts", "create", [], [])

        @classmethod
        def query(cls, criteria):
            return cls.execute("", cls(criteria))

    def push_accounts(self, payload):
        self.set_config()

        # Load encryption config
        with open('config.json') as config_file:
            config = FieldLevelEncryptionConfig(json.load(config_file))

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
