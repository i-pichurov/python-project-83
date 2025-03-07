import validators
from urllib.parse import urlparse


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def is_validate(url):
    errors = {}
    if not validators.url(url):
        errors['name'] = 'Некорректный URL'
    if len(url) > 255:
        errors['name'] = 'Превышена допустимая длина URL'
    return errors
