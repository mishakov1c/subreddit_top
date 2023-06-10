import dataclasses
import datetime
import requests
import requests.auth
import time
from constants import DAYS_LIMIT
from typing import Dict


@dataclasses.dataclass
class Authors:
    comments_authors: list[str]
    posts_authors: list[str]


OAUTH_ENDPOINT = 'https://oauth.reddit.com'


def get_posts_and_comments_authors(token: str) -> Authors | None:
    limit_timestamp = int(time.time() - datetime.timedelta(days=DAYS_LIMIT).total_seconds())

    params_get: Dict[str, str | int] = {
        'limit': 100,
        'sort': 'new',
    }

    headers_get = {
        'User-Agent': 'A subred parcer script',
        'Authorization': f'Bearer {token}'
    }

    comments_authors = []
    posts_authors = []

    while True:
        response = requests.get(
            f'{OAUTH_ENDPOINT}/r/Python/new/',
            headers=headers_get,
            params=params_get,
        )

        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            after = data['data']['after']

            for post in posts:
                post_id = post['data']['id']
                if post['data']['created_utc'] <= limit_timestamp:
                    after = None
                    break

                posts_authors.append(post['data']['author'])

                comment_authors = get_comments_authors(token, post_id, limit_timestamp)
                if comment_authors:
                    comments_authors.extend(comment_authors)

            if after:
                params_get['after'] = after
            else:
                break

        else:
            print(f'Произошла ошибка при получении данных: {response.status_code}')
            return None

    authors = Authors(posts_authors=posts_authors, comments_authors=comments_authors)

    return authors


def get_comments_authors(token: str, post_id: str, limit_timestamp: int) -> list[str]:
    headers_get = {
        'User-Agent': 'A subred parcer script',
        'Authorization': f'Bearer {token}'
    }

    params_get = {
        'limit': 100,
        'after': None
    }

    comment_authors = []

    while True:
        response = requests.get(
            f'{OAUTH_ENDPOINT}/r/Python/comments/{post_id}',
            headers=headers_get,
            params=params_get,
        )

        if response.status_code == 200:
            data = response.json()
            comments = data[1]['data']['children']
            after = data[1]['data'].get('after')

            for comment in comments:
                if comment['data']['created'] <= limit_timestamp:
                    break
                author = comment['data'].get('author')
                if author:
                    comment_authors.append(author)

            if after:
                params_get['after'] = after
            else:
                break
        else:
            print(f'Произошла ошибка при получении комментариев: {response.status_code}')
            return []

    return comment_authors
