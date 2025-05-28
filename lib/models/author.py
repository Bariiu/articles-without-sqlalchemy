from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    def save(self):
        with get_connection() as conn:
            cur = conn.cursor()
            if self.id:
                cur.execute("UPDATE authors SET name=? WHERE id=?", 
                          (self.name, self.id))
            else:
                cur.execute("INSERT INTO authors (name) VALUES (?)", 
                          (self.name,))
                self.id = cur.lastrowid
            return self

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM authors WHERE id=?", (id,)).fetchone()
            return cls(**row) if row else None

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM authors WHERE name=?", (name,)).fetchone()
            return cls(**row) if row else None

    def articles(self):
        from .article import Article
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM articles WHERE author_id=?", (self.id,)).fetchall()
            return [Article(**row) for row in rows]

    def magazines(self):
        from .magazine import Magazine
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT DISTINCT magazines.* FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id=?""", (self.id,)).fetchall()
            return [Magazine(**row) for row in rows]

    def add_article(self, magazine, title):
        from .article import Article
        return Article(title, self.id, magazine.id).save()

    def topic_areas(self):
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT DISTINCT category FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id=?""", (self.id,)).fetchall()
            return [row['category'] for row in rows]

    @classmethod
    def most_published(cls):
        with get_connection() as conn:
            row = conn.execute("""
                SELECT author_id, COUNT(*) as count FROM articles
                GROUP BY author_id ORDER BY count DESC LIMIT 1
            """).fetchone()
            return cls.find_by_id(row['author_id']) if row else None