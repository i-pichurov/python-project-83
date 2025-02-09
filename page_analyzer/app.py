from dotenv import load_dotenv
import os
from flask import Flask, render_template

# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def home_page():
    return render_template(
        'index.html'
    )
