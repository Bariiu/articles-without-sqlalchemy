import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection
from lib.db.schema import setup_schema

@pytest.fixture(autouse=True)
def setup_db():
    """
    Cleans up database data before each test.
    Ensures the schema exists before attempting to delete data.
    """
    setup_schema()

    with get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()
    yield

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
    assert found is not None
    assert found.title == "Test Article"
    assert found.id == sample_article.id

def test_author_relationship(sample_article):
    author = sample_article.author()
    assert author.name == "Test Author"
    assert author.id == sample_article.author_id

def test_magazine_relationship(sample_article):
    magazine = sample_article.magazine()
    assert magazine.name == "Test Magazine"
    assert magazine.id == sample_article.magazine_id

def test_title_validation():
    author_for_validation = Author("Validator Author").save()
    magazine_for_validation = Magazine("Validator Mag", "Validation").save()

    with pytest.raises(ValueError, match="Title must be between 1-255 characters"):
        Article("", author_for_validation.id, magazine_for_validation.id)
    with pytest.raises(ValueError, match="Title must be between 1-255 characters"):
        Article("A" * 256, author_for_validation.id, magazine_for_validation.id)

def test_save_update():
    author = Author("Original Author").save()
    magazine = Magazine("Original Mag", "Original Cat").save()
    article = Article("Original Title", author.id, magazine.id).save()
    
    article.title = "Updated Title"
    updated_article = article.save()
    
    found = Article.find_by_id(article.id)
    assert found.title == "Updated Title"
    assert updated_article.title == "Updated Title"