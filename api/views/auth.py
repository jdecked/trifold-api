from google.oauth2 import id_token
from google.auth.transport import requests
import os


def verify_token(token):
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            os.environ.get('CLIENT_ID')
        )

        if id_info['iss'] not in [
            'accounts.google.com', 'https://accounts.google.com'
        ]:
            raise ValueError('Non-Google wrong issuer.')

        # ID token is valid.
        return id_info

    except ValueError:
        # Invalid token
        pass
