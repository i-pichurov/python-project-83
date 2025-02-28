from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
from psycopg2 import Error
from functools import wraps


# Декоратор для повторного подключения
def retry_db_connection(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # Выполняем функцию
                    return func(*args, **kwargs)
                except OperationalError as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        print(f"Ошибка подключения к базе данных: {e}. Попытки исчерпаны.")
                        raise  # Пробрасываем исключение, если попытки исчерпаны
                    print(f"Ошибка подключения: {e}. Попытка повторного подключения #{retry_count}...")
                except Exception as e:
                    print(f"Произошла ошибка: {e}")
                    raise  # Пробрасываем другие исключения
        return wrapper
    return decorator


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    @retry_db_connection(max_retries=3)
    def get_content(self):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM urls
                    ORDER BY id DESC
                    """
                )
                result = cur.fetchall()
            return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise

    @retry_db_connection(max_retries=3)
    def create(self, url_data):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO urls (
                        name,
                        created_at
                    )
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (
                        url_data['name'],
                        url_data['created_at']
                    )
                )
                url_data['id'] = cur.fetchone()[0]
            self.conn.commit()
            return url_data['id']

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise

    @retry_db_connection(max_retries=3)
    def check_by_name(self, url_data):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM urls
                    WHERE name = %s
                    """,
                    (url_data['name'],)
                )
                result = cur.fetchone()
            return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise

    @retry_db_connection(max_retries=3)
    def find(self, id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                result = cur.fetchone()
            return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise

    @retry_db_connection(max_retries=3)
    def create_url_check(self, url_check):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO url_checks (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description,
                        created_at
                    ) VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        url_check['url_id'],
                        url_check['status_code'],
                        url_check['h1'], url_check['title'],
                        url_check['description'],
                        url_check['created_at']
                    )
                )
            self.conn.commit()

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise

    @retry_db_connection(max_retries=3)
    def get_url_checks(self, url_id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC
                    """,
                    (url_id,)
                )
                result = cur.fetchall()
                return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise

    @retry_db_connection(max_retries=3)
    def get_last_url_check(self, url_id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        urls.name,
                        urls.id,
                        url_checks.created_at,
                        url_checks.status_code
                    FROM urls
                    LEFT JOIN url_checks
                        ON urls.id = url_checks.url_id
                    WHERE urls.id = %s
                    ORDER BY url_checks.created_at DESC
                    LIMIT 1;
                    """,
                    (url_id,)
                )
                result = cur.fetchone()
                return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise
