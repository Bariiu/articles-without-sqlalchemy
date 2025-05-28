from lib.models import Author, Magazine, Article

def seed_data():
    authors = [
        Author("John Doe"),
        Author("Jane Smith")
    ]
    
    magazines = [
        Magazine("Tech Today", "Technology"),
        Magazine("Fashion Weekly", "Fashion")
    ]
    
    articles = [
        Article("Python Basics", 1, 1),
        Article("Advanced Python", 1, 1),
        Article("Summer Trends", 2, 2),
        Article("Winter Collection", 2, 2)
    ]
    
    for obj in authors + magazines + articles:
        obj.save()

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully")