from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn


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
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM urls WHERE name = %s", (url_data['name'],)
            )
            return cur.fetchone()


    def find(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            return cur.fetchone()

