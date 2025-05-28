from lib.db.connection import get_connection

def seed_data():
    """
    Seeds the database with sample authors, magazines, and articles.
    """
    from lib.models.author import Author
    from lib.models.magazine import Magazine
    from lib.models.article import Article

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()

        author1 = Author("John Doe").save()
        author2 = Author("Jane Smith").save()

        magazine1 = Magazine("Tech Weekly", "Technology").save()
        magazine2 = Magazine("Fashion Monthly", "Fashion").save()
        magazine3 = Magazine("Science Today", "Science").save()

        Article("The Future of AI", author1.id, magazine1.id).save()
        Article("Winter Fashion Trends", author2.id, magazine2.id).save()
        Article("Exploring the Cosmos", author1.id, magazine3.id).save()
        Article("New Innovations in Robotics", author1.id, magazine1.id).save()
        Article("Sustainable Living", author2.id, magazine3.id).save()
        Article("Advanced Python Techniques", author1.id, magazine1.id).save()


if __name__ == '__main__':
    seed_data()