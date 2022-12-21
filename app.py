import os
import psycopg2
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url)

@app.route('/')
def home():
    return 'hello world'

@app.post('/api/authors')
def create_author():
    data = request.get_json()

    name = data['name']

    print(name)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO authors (name) VALUES (%s) RETURNING id', (name,))
            conn.commit()
            author_id = cursor.fetchone()[0]
    return {'id': author_id, 'message': f'author {name} was successfully added' }, 201

@app.put('/api/authors/<int:author_id>')
def update_author(author_id):
    data = request.get_json()

    name = data['name']

    with conn:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE authors SET name=%s WHERE id=%s', (name, author_id))
            conn.commit()

    return {'id': author_id, 'message': f'author {name} was successfully updated' }, 200

@app.delete('/api/authors/<int:author_id>')
def delete_author(author_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM authors WHERE id=%s', (author_id,))
            conn.commit()

    return {'message': f'author {author_id} was successfully deleted' }, 200

@app.get('/api/authors')
def get_authors():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM authors')
            authors = cursor.fetchall()

    return {'authors': authors}, 200

@app.get('/api/authors/<int:author_id>')
def get_author(author_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM authors WHERE id=%s', (author_id,))
            author = cursor.fetchone()

    return {'author': author}, 200

@app.post('/api/books')
def create_book():
    data = request.get_json()

    title = data['title']
    author_id = data['author_id']

    with conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO books (title, author_id) VALUES (%s, %s) RETURNING id', (title, author_id))
            book_id = cursor.fetchone()[0]
            conn.commit()

    return {'id': book_id, 'message': f'book {title} was successfully added' }, 201

@app.put('/api/books/<int:book_id>')
def update_book(book_id):
    data = request.get_json()

    title = data['title']
    author_id = data['author_id']

    with conn:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE books SET title=%s, author_id=%s WHERE id=%s', (title, author_id, book_id))
            conn.commit()

    return {'id': book_id, 'message': f'book {title} was successfully updated' }, 200


@app.delete('/api/books/<int:book_id>')
def delete_book(book_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM books WHERE id=%s', (book_id,))
            conn.commit()

    return {'message': f'book {book_id} was successfully deleted' }, 200

@app.get('/api/books')
def get_books():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM books')
            books = cursor.fetchall()

    return {'books': books}, 200

@app.get('/api/books/<int:book_id>')
def get_book(book_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM books WHERE id=%s', (book_id,))
            book = cursor.fetchone()

    return {'book': book}, 200
