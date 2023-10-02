class FluviusAuthenticationToken:
    def __init__(self, token_type: str, expires_in: int, ext_expires_in: int, access_token: str):
        self.token_type = token_type
        self.expires_in = expires_in
        self.ext_expires_in = ext_expires_in
        self.access_token = access_token
