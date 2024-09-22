import os
import django
import mongoengine as m

# переменная окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')

# Инициализация Django
try:
    django.setup()
    print("Django setup completed")
except Exception as e:
    print(f"Error during Django setup: {e}")
    exit(1)

# Подключение к MongoDB
try:
    m.connect(
        db='nataly-db',
        username='nataly-db',
        password='Y2FAaVc9S4eiADtz',
        host='mongodb+srv://cluster0.d0plr.mongodb.net',
        ssl=True
    )
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

# Миграция авторов
try:
    from quotes_app.models import Author as PgAuthor, Quote as PgQuote
    from mongomodels import Author as MongoAuthor, Quote as MongoQuote

    mongo_authors = MongoAuthor.objects
    print(f"Found {mongo_authors.count()} authors in MongoDB")
    for author in mongo_authors:
        PgAuthor.objects.create(
            fullname=author.fullname,
            born_date=author.born_date,
            born_location=author.born_location,
            description=author.description
        )
    print("Authors migration completed")
except Exception as e:
    print(f"Error during authors migration: {e}")
    exit(1)

# Миграция цитат
try:
    mongo_quotes = MongoQuote.objects
    print(f"Found {mongo_quotes.count()} quotes in MongoDB")
    for quote in mongo_quotes:
        pg_author = PgAuthor.objects.get(fullname=quote.author.fullname)
        PgQuote.objects.create(
            tags=quote.tags,
            author=pg_author,
            quote=quote.quote
        )
    print("Quotes migration completed")
except Exception as e:
    print(f"Error during quotes migration: {e}")
    exit(1)
