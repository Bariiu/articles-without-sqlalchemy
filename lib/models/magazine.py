from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.name} ({self.category})>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not 1 <= len(value) <= 255:
            raise ValueError("Name must be between 1-255 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not 1 <= len(value) <= 255:
            raise ValueError("Category must be between 1-255 characters")
        self._category = value

    def save(self):
        with get_connection() as conn:
            cur = conn.cursor()
            if self.id:
                cur.execute("UPDATE magazines SET name=?, category=? WHERE id=?", 
                          (self.name, self.category, self.id))
            else:
                cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", 
                          (self.name, self.category))
                self.id = cur.lastrowid
            return self

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM magazines WHERE id=?", (id,)).fetchone()
            return cls(**row) if row else None

    def articles(self):
        from .article import Article
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,)).fetchall()
            return [Article(**row) for row in rows]

    def contributors(self):
        from .author import Author
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT DISTINCT authors.* FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id=?""", (self.id,)).fetchall()
            return [Author(**row) for row in rows]

    def article_titles(self):
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        from .author import Author
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT authors.* FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id=?
                GROUP BY authors.id HAVING COUNT(articles.id) > 2
            """, (self.id,)).fetchall()
            return [Author(**row) for row in rows]

    @classmethod
    def article_counts(cls):
        with get_connection() as conn:
            return {row['name']: row['count'] for row in conn.execute("""
                SELECT magazines.name, COUNT(articles.id) as count
                FROM magazines LEFT JOIN articles
                ON magazines.id = articles.magazine_id
                GROUP BY magazines.id
            """)}

    @classmethod
    def find_with_multiple_authors(cls):
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT magazines.* FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                GROUP BY magazines.id
                HAVING COUNT(DISTINCT articles.author_id) >= 2
            """).fetchall()
            return [cls(**row) for row in rows]