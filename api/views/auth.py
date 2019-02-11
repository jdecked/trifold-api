from google.oauth2 import id_token
from google.auth.transport import requests

# TODO (jdc): Hide CLIENT_ID in an env variable
CLIENT_ID = \
    '121062910806-hi9gi8sm3g1or6k88bilq8quk1do71bs.apps.googleusercontent.com'


def verify_token(token):
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            CLIENT_ID
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
