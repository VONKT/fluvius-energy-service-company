import base64
import http.client
import json
import time
import urllib.parse
import uuid

import jwt

from fluvius_energy_service_company.fluvius_config import FluviusConfig

class FluviusAuthenticationToken():
    def __init__(self, token_type: str, expires_in: int, ext_expires_in: int, access_token: str):
        self.token_type = token_type
        self.expires_in = expires_in
        self.ext_expires_in = ext_expires_in
        self.access_token = access_token

class FluviusAuthentication:

    def __init__(self, fluvius_config: FluviusConfig):
        self.fluvius_config = fluvius_config
        self.token: FluviusAuthenticationToken = None

    @staticmethod
    def _encode_thumbprint(hex_thumbprint: str) -> str:
        return str(base64.b64encode(bytearray.fromhex(hex_thumbprint)), 'utf-8')

    def _get_signed_jwt(self) -> str:

        decoded_token_header = {
            'alg': 'RS256',
            'typ': 'JWT',
            'x5t': self._encode_thumbprint(self.fluvius_config.certificate_thumb_print),
        }

        token_creation_time = int(time.time())
        token_end_time = token_creation_time + 3600

        decoded_token_body = {
            'aud': f'https://login.microsoftonline.com/{self.fluvius_config.tenant_id}/v2.0',
            'exp': token_end_time,
            'iss': self.fluvius_config.client_id,
            'jti': str(uuid.uuid4()),
            'nbf': token_creation_time,
            'sub': self.fluvius_config.client_id,
        }

        return jwt.encode(decoded_token_body, self.fluvius_config.certificate_key, headers=decoded_token_header)

    def _get_fluvius_token(self) -> FluviusAuthenticationToken:
        token_creation_time = int(time.time())
        self.current_token_end_time = token_creation_time + 3600
        conn = http.client.HTTPSConnection("login.microsoftonline.com")
        query = {
            'scope': self.fluvius_config.live_scope,
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'grant_type': 'client_credentials',
            'client_id': self.fluvius_config.client_id,
            'client_assertion': self._get_signed_jwt()
        }
        query_string = urllib.parse.urlencode(query)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        conn.request("POST", f'/{self.fluvius_config.tenant_id}/oauth2/v2.0/token', query_string, headers)
        res = conn.getresponse()
        data = res.read()
        json_object = json.loads(data.decode("utf-8"))
        return FluviusAuthenticationToken(**json_object)

    def _token_is_valid(self):
        if not self.token:
            return False
        if not self.current_token_end_time:
            return False
        safety_margin = 60
        now = int(time.time())
        return (now + safety_margin) < self.current_token_end_time

    def create_authorization_header(self):
        token = self.get_token()
        return {
            'Authorization': f'Bearer {token.access_token}',
            'Ocp-Apim-Subscription-Key': self.fluvius_config.subscription_key,
            'Content-Type': 'application/json',
        }

    def get_token(self):
        if self._token_is_valid():
            print('Reuse current token')
            return self.token
        print('Creating new token')
        self.token = self._get_fluvius_token()
        return self.token