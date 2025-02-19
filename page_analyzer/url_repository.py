from psycopg2.extras import RealDictCursor
from psycopg2 import Error


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn


    def get_content(self):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls ORDER BY id DESC")
                result = cur.fetchall()
            return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise


    def create(self, url_data):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (url_data['name'], url_data['created_at'])
            )
            url_data['id'] = cur.fetchone()[0]
        self.conn.commit()
        return url_data['id']


    def check_by_name(self, url_data):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM urls WHERE name = %s", (url_data['name'],)
                )
                result = cur.fetchone()
            return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise


    def find(self, id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                result = cur.fetchone()
            return result

        except Error as e:
            print(f"Database error: {e}")  # Логирование ошибки
            raise
