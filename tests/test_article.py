import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture(autouse=True)
def setup_db():
    with Article.get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()

@pytest.fixture
def sample_article():
    author = Author("Test Author").save()
    magazine = Magazine("Test Magazine", "Testing").save()
    return Article("Test Article", author.id, magazine.id).save()

def test_article_creation(sample_article):
    assert sample_article.id is not None
    assert sample_article.title == "Test Article"

def test_find_by_id(sample_article):
    found = Article.find_by_id(sample_article.id)
    assert found.title == "Test Article"

def test_author_relationship(sample_article):
    author = sample_article.author()
    assert author.name == "Test Author"

def test_magazine_relationship(sample_article):
    magazine = sample_article.magazine()
    assert magazine.name == "Test Magazine"

def test_title_validation():
    with pytest.raises(ValueError):
        Article("", 1, 1)
    with pytest.raises(ValueError):
        Article("A" * 256, 1, 1)

def test_save_update():
    article = Article("Original Title", 1, 1).save()
    article.title = "Updated Title"
    updated = article.save()
    assert Article.find_by_id(article.id).title == "Updated Title"