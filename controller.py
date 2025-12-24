# controller.py
from database import *

def add_book_controller(title, author, year):
    if not title or not author or not year:
        return False
    insert_book(title, author, year)
    return True

def get_books_controller():
    return fetch_books()

def search_books_controller(keyword):
    return search_books(keyword)

def delete_book_controller(book_id):
    delete_book(book_id)