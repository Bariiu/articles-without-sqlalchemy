from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.title}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not 1 <= len(value) <= 255:
            raise ValueError("Title must be between 1-255 characters")
        self._title = value

    def save(self):
        with get_connection() as conn:
            cur = conn.cursor()
            if self.id:
                cur.execute("""
                    UPDATE articles SET title=?, author_id=?, magazine_id=?
                    WHERE id=?""", (self.title, self.author_id, self.magazine_id, self.id))
            else:
                cur.execute("""
                    INSERT INTO articles (title, author_id, magazine_id)
                    VALUES (?, ?, ?)""", (self.title, self.author_id, self.magazine_id))
                self.id = cur.lastrowid
            return self

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM articles WHERE id=?", (id,)).fetchone()
            return cls(**row) if row else None

    def author(self):
        from .author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from .magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)