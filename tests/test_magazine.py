import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture(autouse=True)
def setup_db():
    with Magazine.get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()

@pytest.fixture
def sample_data():
    author1 = Author("J.K. Rowling").save()
    author2 = Author("Stephen King").save()
    magazine1 = Magazine("Fantasy Today", "Fantasy").save()
    magazine2 = Magazine("Horror Monthly", "Horror").save()
    
    Article("Harry Potter", author1.id, magazine1.id).save()
    Article("Fantasy Writing", author1.id, magazine1.id).save()
    Article("The Shining", author2.id, magazine2.id).save()
    Article("Horror 101", author2.id, magazine2.id).save()
    
    return {
        "authors": [author1, author2],
        "magazines": [magazine1, magazine2]
    }

def test_magazine_creation():
    magazine = Magazine("Tech Weekly", "Technology").save()
    assert magazine.id is not None
    assert magazine.name == "Tech Weekly"
    assert magazine.category == "Technology"

def test_find_by_id(sample_data):
    magazine = Magazine.find_by_id(sample_data["magazines"][0].id)
    assert magazine.name == "Fantasy Today"

def test_articles_relationship(sample_data):
    magazine = sample_data["magazines"][0]
    articles = magazine.articles()
    assert len(articles) == 2
    assert {a.title for a in articles} == {"Harry Potter", "Fantasy Writing"}

def test_contributors(sample_data):
    magazine = sample_data["magazines"][0]
    contributors = magazine.contributors()
    assert len(contributors) == 1
    assert contributors[0].name == "J.K. Rowling"

def test_article_titles(sample_data):
    magazine = sample_data["magazines"][1]
    titles = magazine.article_titles()
    assert titles == ["The Shining", "Horror 101"]

def test_contributing_authors(sample_data):
    magazine = sample_data["magazines"][1]
    author = sample_data["authors"][1]
    Article("Another Horror", author.id, magazine.id).save()
    Article("More Horror", author.id, magazine.id).save()
    
    contributors = magazine.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "Stephen King"

def test_article_counts(sample_data):
    counts = Magazine.article_counts()
    assert counts["Fantasy Today"] == 2
    assert counts["Horror Monthly"] == 2

def test_find_with_multiple_authors():
    author1 = Author("Author A").save()
    author2 = Author("Author B").save()
    magazine = Magazine("Multi Author Mag", "General").save()
    
    Article("Article 1", author1.id, magazine.id).save()
    Article("Article 2", author2.id, magazine.id).save()
    
    results = Magazine.find_with_multiple_authors()
    assert len(results) == 1
    assert results[0].name == "Multi Author Mag"