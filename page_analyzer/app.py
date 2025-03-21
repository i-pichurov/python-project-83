import os
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from datetime import date
from page_analyzer.url_repository import UrlRepository
from page_analyzer.parser import parse
from page_analyzer.validator import (
    normalize_url,
    is_validate
)
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)


# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

repo = UrlRepository(app.config['DATABASE_URL'])


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def urls_get():
    urls = repo.get_urls_list()
    last_url_checks = []

    for url in urls:
        last_url_check = repo.get_last_url_check(url['id'])
        last_url_checks.append(last_url_check)

    return render_template(
        'urls/urls_list.html',
        last_url_checks=last_url_checks
    )


@app.post('/urls')
def urls_post():

    raw_url = request.form.get('url')
    errors = is_validate(raw_url)

    if errors:
        flash(errors['name'], 'danger')
        return render_template(
            'index.html',
            url=raw_url
        ), 422

    url = {
        'name': normalize_url(raw_url),
        'created_at': date.today()
    }

    existing_url = repo.get_by_name(url)
    if existing_url:
        id = existing_url['id']
        flash('Страница уже существует', 'info')
    else:
        id = repo.create(url)
        flash('Страница успешно добавлена', 'success')

    return redirect(url_for('urls_show', id=id), code=302)


@app.route('/urls/<id>')
def urls_show(id):
    url = repo.get_by_id(id)
    url_checks = repo.get_url_checks(id)

    return render_template(
        'urls/show.html',
        url=url,
        url_checks=url_checks
    )


@app.post('/urls/<id>/checks')
def url_checks(id):

    url = repo.get_by_id(id)

    try:
        response = requests.get(url['name'])
        response.raise_for_status()
        url_check = {
            'url_id': id,
            'status_code': response.status_code,
            'created_at': date.today()
        }
        url_check.update(parse(response.text))
        repo.create_url_check(url_check)
        flash('Страница успешно проверена', 'success')

    except RequestException as e:
        print(f'Произошла ошибка при выполнении запроса: {e}')
        flash('Произошла ошибка при проверке', 'danger')

    finally:
        return redirect(url_for('urls_show', id=id), code=302)
