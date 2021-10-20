from os import environ
import databases


DB_USER = environ.get('DB_USER', 'mracs_test')
DB_PASSWORD = environ.get('DB_PASSWORD', 'mracs_test')
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_NAME = 'swaplify_test' if environ.get('TESTING') else environ.get(
    'DB_NAME', 'mracs')
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)
