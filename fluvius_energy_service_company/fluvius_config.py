import os

class FluviusConfig:

    def __init__(self, 
                 subscription_key: str = None,
                 certificate_thumb_print: str = None,
                 live_scope: str = None,
                 client_id: str = None,
                 tenant_id: str = None,
                 data_access_contract_number: str = None,
                 certificate_key: str = None,
                 certificate_key_path: str = None,
                 ) -> None:
        if os.getenv('SUBSCRIPTION_KEY') is None and subscription_key is None:
            raise ValueError('No subscription key set, not able to initialize Fluvius API')
        if os.getenv('CERTIFICATE_THUMB_PRINT') is None and certificate_thumb_print is None:
            raise ValueError('No certificate thumb print is set, not able to initialize Fluvius API')
        if os.getenv('LIVE_SCOPE') is None and live_scope is None:
            raise ValueError('No live scope is set, not able to initialize Fluvius API')
        if os.getenv('CLIENT_ID') is None and client_id is None:
            raise ValueError('No client id is set, not able to initialize Fluvius API')
        if os.getenv('TENANT_ID') is None and tenant_id is None:
            raise ValueError('No tenant id is set, not able to initialize Fluvius API')
        if os.getenv('DATA_ACCESS_CONTRACT_NUMBER') is None and data_access_contract_number is None:
            raise ValueError('No data access contract number is set, not able to initialize Fluvius API')
        if (os.getenv('CERTIFICATE_KEY') is None and certificate_key is None) and (os.getenv('CERTIFICATE_KEY_PATH') is None and certificate_key_path is None):
            raise ValueError('No certificate key or key lccation is set, not able to initialize Fluvius API')
        self.subscription_key = subscription_key if subscription_key is not None else os.getenv('SUBSCRIPTION_KEY')
        self.certificate_thumb_print = certificate_thumb_print if certificate_thumb_print is not None else os.getenv('CERTIFICATE_THUMB_PRINT')
        if not self._is_hexadecimal(self.certificate_thumb_print):
            raise ValueError('Certificate thumb print is not a valid hexadecimal string')
        self.live_scope = live_scope if live_scope is not None else os.getenv('LIVE_SCOPE')
        self.client_id = client_id if client_id is not None else os.getenv('CLIENT_ID')
        self.tenant_id = tenant_id if tenant_id is not None else os.getenv('TENANT_ID')
        self.data_access_contract_number = data_access_contract_number if data_access_contract_number is not None else os.getenv('DATA_ACCESS_CONTRACT_NUMBER')

        # Certificate key can be set as a string or as a path to a file
        # If both are set, the string will be used
        self.certificate_key = certificate_key if certificate_key is not None else os.getenv('CERTIFICATE_KEY')
        self.certificate_key_path = certificate_key_path if certificate_key_path is not None else os.getenv('CERTIFICATE_KEY_PATH')
        if self.certificate_key is None:
            with open(self.certificate_key_path, 'r') as keyfile:
                self.certificate_key = keyfile.read()

    @staticmethod
    def _is_hexadecimal(value):
        try:
            int(value, 16)
            return True
        except ValueError:
            return False