import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture(autouse=True)
def setup_db():
    with Author.get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()

def test_author_save():
    author = Author("Test Author").save()
    assert Author.find_by_id(author.id) is not None

def test_author_articles():
    author = Author("Test Author").save()
    magazine = Magazine("Tech", "Tech").save()
    article = author.add_article(magazine, "Python Rocks")
    assert len(author.articles()) == 1
    assert author.articles()[0].title == "Python Rocks"

def test_magazine_contributors():
    author1 = Author("A1").save()
    author2 = Author("A2").save()
    magazine = Magazine("M1", "Tech").save()
    Article("Art1", author1.id, magazine.id).save()
    Article("Art2", author2.id, magazine.id).save()
    assert len(magazine.contributors()) == 2

def test_most_published():
    a1 = Author("A1").save()
    a2 = Author("A2").save()
    m = Magazine("M", "Tech").save()
    Article("A1", a1.id, m.id).save()
    Article("A2", a1.id, m.id).save()
    Article("A3", a2.id, m.id).save()
    assert Author.most_published().name == "A1"