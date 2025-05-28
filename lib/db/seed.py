from lib.db.connection import get_connection
# No top-level imports of Author, Magazine, Article here to avoid circular imports

def seed_data():
    """
    Seeds the database with sample authors, magazines, and articles.
    """
    # Import models locally within the function to avoid circular dependency
    from lib.models.author import Author
    from lib.models.magazine import Magazine
    from lib.models.article import Article

    with get_connection() as conn:
        cursor = conn.cursor()

        # Clear existing data before seeding to ensure a clean slate
        # Note: In a test environment, individual test fixtures handle deletion.
        # This is primarily for manual seeding.
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()

        # Seed Authors
        author1 = Author("John Doe").save()
        author2 = Author("Jane Smith").save()

        # Seed Magazines
        magazine1 = Magazine("Tech Weekly", "Technology").save()
        magazine2 = Magazine("Fashion Monthly", "Fashion").save()
        magazine3 = Magazine("Science Today", "Science").save()

        # Seed Articles
        Article("The Future of AI", author1.id, magazine1.id).save()
        Article("Winter Fashion Trends", author2.id, magazine2.id).save()
        Article("Exploring the Cosmos", author1.id, magazine3.id).save()
        Article("New Innovations in Robotics", author1.id, magazine1.id).save()
        Article("Sustainable Living", author2.id, magazine3.id).save()
        Article("Advanced Python Techniques", author1.id, magazine1.id).save()

        # print("Database seeded successfully!") # Comment out for cleaner test output

if __name__ == '__main__':
    seed_data()