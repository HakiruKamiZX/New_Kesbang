from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['newsDB']
collection = db['articles']

# Example articles
articles = [
    {
        "title": "Exploring the Wonders of the Grand Canyon",
        "date": datetime.now().strftime('%B %d, %Y'),
        "author": "Jane Doe",
        "category": "Travel",
        "content": "The Grand Canyon is one of the most iconic natural wonders of the world...",
        "image": "/static/images/grand-canyon.jpg"
    },
    {
        "title": "A Day in the Life of a Software Developer",
        "date": datetime.now().strftime('%B %d, %Y'),
        "author": "John Smith",
        "category": "Technology",
        "content": "Software development is an exciting field with numerous challenges and rewards...",
        "image": "/static/images/software-development.jpg"
    }
]

# Insert multiple documents into the collection
collection.insert_many(articles)
