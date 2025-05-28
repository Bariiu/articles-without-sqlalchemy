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
def sample_author():
    return Author("Stephen King").save()

def test_author_creation(sample_author):
    assert sample_author.id is not None
    assert sample_author.name == "Stephen King"

def test_author_find_by_id(sample_author):
    found_author = Author.find_by_id(sample_author.id)
    assert found_author is not None
    assert found_author.name == "Stephen King"
    assert found_author.id == sample_author.id

def test_author_find_by_name():
    author = Author("George R.R. Martin").save()
    found_author = Author.find_by_name("George R.R. Martin")
    assert found_author is not None
    assert found_author.name == "George R.R. Martin"
    assert found_author.id == author.id

def test_author_name_validation():
    with pytest.raises(ValueError, match="Name must be a non-empty string"):
        Author("").save()
    with pytest.raises(ValueError, match="Name must be a non-empty string"):
        Author("   ").save()

def test_author_save_update():
    author = Author("Original Name").save()
    author.name = "Updated Name"
    updated_author = author.save()
    
    found = Author.find_by_id(author.id)
    assert found.name == "Updated Name"
    assert updated_author.name == "Updated Name"

def test_articles_relationship(sample_author):
    magazine1 = Magazine("Horror Lit", "Horror").save()
    magazine2 = Magazine("Fantasy Reads", "Fiction").save()
    article1 = sample_author.add_article(magazine1, "It")
    article2 = sample_author.add_article(magazine2, "The Dark Tower")
    
    articles = sample_author.articles()
    assert len(articles) == 2
    assert any(a.title == "It" for a in articles)
    assert any(a.title == "The Dark Tower" for a in articles)
    assert all(isinstance(a, Article) for a in articles)

def test_magazines_relationship(sample_author):
    magazine1 = Magazine("Horror Lit", "Horror").save()
    magazine2 = Magazine("Fantasy Reads", "Fiction").save()
    sample_author.add_article(magazine1, "Pet Sematary")
    sample_author.add_article(magazine2, "The Stand")
    
    magazines = sample_author.magazines()
    assert len(magazines) == 2
    assert any(m.name == "Horror Lit" for m in magazines)
    assert any(m.name == "Fantasy Reads" for m in magazines)
    assert all(isinstance(m, Magazine) for m in magazines)

def test_add_article(sample_author):
    magazine = Magazine("Sci-Fi Weekly", "Sci-Fi").save()
    article = sample_author.add_article(magazine, "New Sci-Fi Story")
    assert article.title == "New Sci-Fi Story"
    assert article.author_id == sample_author.id
    assert article.magazine_id == magazine.id
    assert Article.find_by_id(article.id) is not None

def test_topic_areas(sample_author):
    magazine1 = Magazine("Tech Today", "Technology").save()
    magazine2 = Magazine("Nature's Wonders", "Science").save()
    magazine3 = Magazine("Digital Life", "Technology").save()
    sample_author.add_article(magazine1, "AI Advances")
    sample_author.add_article(magazine2, "Exploring the Amazon")
    sample_author.add_article(magazine3, "Cybersecurity Basics")
    
    topic_areas = sample_author.topic_areas()
    assert sorted(topic_areas) == sorted(["Technology", "Science"])
    assert len(topic_areas) == len(set(topic_areas))
    assert all(isinstance(t, str) for t in topic_areas)


def test_most_published():
    author1 = Author("Author A").save()
    author2 = Author("Author B").save()
    magazine = Magazine("Test Mag", "Test Cat").save()

    author1.add_article(magazine, "Article 1 by A")
    author1.add_article(magazine, "Article 2 by A")
    author1.add_article(magazine, "Article 3 by A")
    author2.add_article(magazine, "Article 1 by B")
    author2.add_article(magazine, "Article 2 by B")

    most_published_author = Author.most_published()
    assert most_published_author is not None
    assert most_published_author.name == "Author A"

    Author("Author C").save()
    with get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.commit()
    assert Author.most_published() is None