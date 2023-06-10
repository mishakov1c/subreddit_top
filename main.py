from access import get_access_token
from authors import get_posts_and_comments_authors
from collections import Counter
from operator import itemgetter


def print_tops(get_posts_and_comments_authors, access_token):
    authors = get_posts_and_comments_authors(access_token)
    if authors:
        print('Топ авторов статей:')
        for author, count in sorted(
                Counter(authors.posts_authors).items(),
                key=itemgetter(1),
                reverse=True
        ):
            print(f'{author}, Постов: {count}')
        print('Топ авторов комментариев:')
        for author, count in sorted(
                Counter(authors.comments_authors).items(),
                key=itemgetter(1),
                reverse=True
        ):
            print(f'{author}, Комментариев: {count}')


if __name__ == '__main__':
    access_token = get_access_token()
    if access_token:
        print_tops(get_posts_and_comments_authors, access_token)
    else:
        print('Не удалось получить токен доступа.')
