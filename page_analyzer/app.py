import os
import psycopg2
import validators
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages
)
from datetime import date
from urllib.parse import urlparse
from page_analyzer.url_repository import UrlRepository

# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


conn = psycopg2.connect(app.config['DATABASE_URL'])
repo = UrlRepository(conn)


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )


@app.get('/urls')
def urls_get():
    urls = repo.get_content()
    return render_template(
        'urls/urls_list.html',
        urls=urls
    )


@app.post('/urls')
def urls_post():

    raw_url = request.form.get('url')

    if not validators.url(raw_url):
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url=raw_url,
            messages=messages
        )

    url = {
        'name': normalize_url(raw_url),
        'created_at': date.today()
    }

    existing_url = repo.check_by_name(url)
    if existing_url:
        id = existing_url['id']
        flash('Страница уже существует', 'info')
    else:
        id = repo.create(url)
        flash('Страница успешно добавлена', 'success')

    return redirect(url_for('urls_show', id=id), code=302)


@app.route('/urls/<id>')
def urls_show(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find(id)
    return render_template(
        'urls/show.html',
        url=url,
        messages=messages
    )