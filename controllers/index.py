from app import app
from flask import render_template, request, session
import sqlite3
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, borrow_book, get_new_reader
from models.book import return_book
@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()
    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id
    elif request.values.get('submitNewReader'):
        html=render_template('new_reader.html')
        return html
    elif request.values.get('newReaderFio'):
        r_id=get_new_reader(conn, request.values.get('newReaderFio'))
        print(r_id)
        session['reader_id'] = int(r_id)
    elif request.values.get('return'):
        reader_book_id = int(request.values.get('return'))
        print(reader_book_id)
        return_book(conn, reader_book_id)
    elif request.values.get('book'):
        book_id = int(request.values.get('book'))
        borrow_book(conn, book_id, session['reader_id'])
    elif request.values.get('noselect'):
        a = 1
    else:
        session['reader_id']= 3
    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    html = render_template(
        'index.html',
        reader_id = session['reader_id'],
        combo_box = df_reader,
        book_reader = df_book_reader,
        len = len
    )
    return html