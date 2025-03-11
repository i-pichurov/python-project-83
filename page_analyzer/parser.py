from bs4 import BeautifulSoup


def parse(page_info):

    soup = BeautifulSoup(page_info, 'html.parser')

    h1_tag = soup.find('h1')
    h1_text = h1_tag.get_text() if h1_tag else ''

    title_tag = soup.find('title')
    title_text = title_tag.get_text() if title_tag else ''

    description_tag = soup.find('meta', attrs={'name': 'description'})
    description_text = description_tag.get('content') \
        if description_tag else ''

    result = {
            'h1': h1_text,
            'title': title_text,
            'description': description_text,
        }

    return result
