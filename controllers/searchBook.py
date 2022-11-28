from app import app
from flask import render_template, request, session, redirect
import sqlite3
from utils import get_db_connection
import models.search_book_model as model
@app.route('/searchBook', methods=['get'])
def searchBook():
    conn = get_db_connection()

    if request.values.get('submitBorrowBook'):
        user_id=int(request.values.get('reader_id'))
        book_id=int(request.values.get('borrow_book_id'))
        model.borrow_book(conn, book_id, user_id)
        return redirect('searchBook')

    checked_authors_s = request.values.getlist('authors[]')
    checked_genres_s = request.values.getlist('genres[]')
    checked_publishers_s = request.values.getlist('publishers[]')

    checked_authors = [ int(x) for x in checked_authors_s ]
    checked_genres = [ int(x) for x in checked_genres_s ]
    checked_publishers = [ int(x) for x in checked_publishers_s ]

    checked_genres = tuple(checked_genres)
    checked_authors = tuple(checked_authors)
    checked_publishers = tuple(checked_publishers)

    # if isinstance(checked_publishers, int):
    #     checked_publishers = (checked_publishers,)
    # if isinstance(checked_genres, int):
    #     checked_genres = (checked_genres,)
    # if isinstance(checked_authors, int):
    #     checked_authors = (checked_authors,)

    df_author = model.get_author(conn)
    df_publisher = model.get_publisher(conn)
    df_genre = model.get_genre(conn)
    df_card = model.cardQuerry(conn, checked_publishers, checked_genres, checked_authors)
    conn.close()

    return render_template(
        'searchBook.html',
        df_authors=df_author,
        df_publishers=df_publisher,
        df_genres=df_genre,
        card=df_card,
        checked_authors=checked_authors,
        checked_publishers=checked_publishers,
        checked_genres=checked_genres,
        len=len,
        int=int,
        user_id=session['reader_id']
    )
