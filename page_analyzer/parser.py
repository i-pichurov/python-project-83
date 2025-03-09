import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def parse(url):
    errors = {}
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tag = soup.find('h1')
        h1_text = h1_tag.get_text() if h1_tag else ''

        title_tag = soup.find('title')
        title_text = title_tag.get_text() if title_tag else ''

        description_tag = soup.find('meta', attrs={'name': 'description'})
        description_text = description_tag.get('content') \
            if description_tag else ''

        result = {
                'status_code': response.status_code,
                'h1': h1_text,
                'title': title_text,
                'description': description_text,
            }

    except RequestException as e:
        print(f'Произошла ошибка при выполнении запроса: {e}')
        result = {}
        errors['name'] = 'Произошла ошибка при проверке'

    finally:
        return result, errors
