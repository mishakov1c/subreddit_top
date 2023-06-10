from config import CLIENT_ID, CLIENT_SECRET, USER_NAME, PASSWORD
import requests


def get_access_token() -> str | None:
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {
        'grant_type': 'password',
        'username': USER_NAME,
        'password': PASSWORD,
    }

    headers = {
        'User-Agent': 'A subred top script',
    }

    TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'

    response = requests.post(
        TOKEN_ACCESS_ENDPOINT,
        data=post_data,
        headers=headers,
        auth=client_auth
    )

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None
