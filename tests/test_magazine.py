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
def sample_magazine():
    return Magazine("National Geographic", "Nature").save()

def test_magazine_creation(sample_magazine):
    assert sample_magazine.id is not None
    assert sample_magazine.name == "National Geographic"
    assert sample_magazine.category == "Nature"

def test_magazine_find_by_id(sample_magazine):
    found = Magazine.find_by_id(sample_magazine.id)
    assert found is not None
    assert found.name == "National Geographic"
    assert found.id == sample_magazine.id

def test_magazine_name_validation():
    with pytest.raises(ValueError, match="Name must be between 1-255 characters"):
        Magazine("", "Category").save()
    with pytest.raises(ValueError, match="Name must be between 1-255 characters"):
        Magazine("A" * 256, "Category").save()

def test_magazine_category_validation():
    with pytest.raises(ValueError, match="Category must be between 1-255 characters"):
        Magazine("Name", "").save()
    with pytest.raises(ValueError, match="Category must be between 1-255 characters"):
        Magazine("Name", "C" * 256).save()

def test_magazine_save_update():
    magazine = Magazine("Original Mag", "Original Cat").save()
    magazine.name = "Updated Mag"
    magazine.category = "Updated Cat"
    updated = magazine.save()
    found = Magazine.find_by_id(magazine.id)
    assert found.name == "Updated Mag"
    assert found.category == "Updated Cat"
    assert updated.name == "Updated Mag"

def test_articles_relationship(sample_magazine):
    author = Author("Test Author").save()
    article1 = Article("Ocean Depths", author.id, sample_magazine.id).save()
    article2 = Article("Wildlife Photography", author.id, sample_magazine.id).save()
    
    articles = sample_magazine.articles()
    assert len(articles) == 2
    assert any(a.title == "Ocean Depths" for a in articles)
    assert any(a.title == "Wildlife Photography" for a in articles)
    assert all(isinstance(a, Article) for a in articles)


def test_contributors(sample_magazine):
    author1 = Author("Photographer A").save()
    author2 = Author("Writer B").save()
    Article("Nature's Beauty", author1.id, sample_magazine.id).save()
    Article("Travel Logs", author2.id, sample_magazine.id).save()
    
    contributors = sample_magazine.contributors()
    assert len(contributors) == 2
    assert any(c.name == "Photographer A" for c in contributors)
    assert any(c.name == "Writer B" for c in contributors)
    assert all(isinstance(c, Author) for c in contributors)

def test_article_titles(sample_magazine):
    author = Author("Some Author").save()
    Article("Title One", author.id, sample_magazine.id).save()
    Article("Title Two", author.id, sample_magazine.id).save()
    
    titles = sample_magazine.article_titles()
    assert sorted(titles) == sorted(["Title One", "Title Two"])
    assert all(isinstance(t, str) for t in titles)

def test_contributing_authors():
    magazine = Magazine("Tech Innovators", "Tech").save()
    author1 = Author("Alice").save()
    author2 = Author("Bob").save()
    author3 = Author("Charlie").save()

    Article("AI in Healthcare", author1.id, magazine.id).save()
    Article("Quantum Computing Basics", author1.id, magazine.id).save()
    Article("Future of Robotics", author1.id, magazine.id).save()

    Article("Web Development Trends", author2.id, magazine.id).save()
    Article("Mobile App Design", author2.id, magazine.id).save()

    Article("Cloud Security", author3.id, magazine.id).save()

    contributing_authors = magazine.contributing_authors()
    assert len(contributing_authors) == 1
    assert contributing_authors[0].name == "Alice"
    assert isinstance(contributing_authors[0], Author)

def test_article_counts():
    magazine1 = Magazine("Science Monthly", "Science").save()
    magazine2 = Magazine("Art Daily", "Art").save()
    magazine3 = Magazine("No Articles Yet", "Empty").save()
    author = Author("Test Author").save()

    Article("Physics Explained", author.id, magazine1.id).save()
    Article("Chemistry Basics", author.id, magazine1.id).save()
    Article("Art History 101", author.id, magazine2.id).save()

    counts = Magazine.article_counts()
    assert counts.get("Science Monthly") == 2
    assert counts.get("Art Daily") == 1
    assert counts.get("No Articles Yet") == 0

def test_find_with_multiple_authors():
    magazine1 = Magazine("Magazine A", "Category A").save()
    magazine2 = Magazine("Magazine B", "Category B").save()
    magazine3 = Magazine("Magazine C", "Category C").save()

    author1 = Author("Author 1").save()
    author2 = Author("Author 2").save()
    author3 = Author("Author 3").save()

    Article("Article A1", author1.id, magazine1.id).save()
    Article("Article A2", author2.id, magazine1.id).save()

    Article("Article B1", author1.id, magazine2.id).save()
    Article("Article B2", author2.id, magazine2.id).save()
    Article("Article B3", author3.id, magazine2.id).save()

    Article("Article C1", author1.id, magazine3.id).save()
    Article("Article C2", author1.id, magazine3.id).save()

    magazines = Magazine.find_with_multiple_authors()
    assert len(magazines) == 2
    magazine_names = {m.name for m in magazines}
    assert "Magazine A" in magazine_names
    assert "Magazine B" in magazine_names
    assert "Magazine C" not in magazine_names
    assert all(isinstance(m, Magazine) for m in magazines)