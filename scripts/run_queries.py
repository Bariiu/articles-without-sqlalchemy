from lib.models import Author, Magazine, Article
from lib.db import seed_data

def main():
    seed_data()
    
    author = Author.find_by_name("John Doe")
    print(f"Articles by {author.name}:")
    for article in author.articles():
        print(f"- {article.title}")
    
    print("\nMagazines contributed to:")
    for magazine in author.magazines():
        print(f"- {magazine.name} ({magazine.category})")
    
    magazine = Magazine.find_by_name("Tech Today")
    print("\nAuthors in Tech Today:")
    for contributor in magazine.contributors():
        print(f"- {contributor.name}")
    
    print("\nMagazines with multiple authors:")
    for magazine in Magazine.find_with_multiple_authors():
        print(f"- {magazine.name}")
    
    print("\nArticle counts:")
    for name, count in Magazine.article_counts().items():
        print(f"- {name}: {count} articles")
    
    prolific = Author.most_published()
    print(f"\nMost published author: {prolific.name}")

if __name__ == "__main__":
    main()