import pandas

from app import app
from flask import render_template, request, session
import sqlite3
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, borrow_book, get_new_reader
from models.book import return_book
from models.statistics import borrowers, most_popular_book

def convert_date(date):
    dates=date.split('.')
    if(len(dates)>3):
        return dates[2]+'-'+dates[1]+'-'+dates[0]
    else:
        return date

@app.route('/statistics', methods=['get'])
def statistics():
    conn = get_db_connection()
    borrowers_list=pandas.DataFrame
    books_list=pandas.DataFrame
    most_popular_book_df=pandas.DataFrame
    if request.values.get('submitGetBorrowers'):
        startDate=request.values.get('dateStart')
        endDate=request.values.get('dateEnd')
        startDate=convert_date(startDate)
        endDate=convert_date(endDate)
        borrowers_list=borrowers(conn, startDate, endDate)
        print(borrowers_list)
        return render_template('statistics.html',
                               borrowers_list=borrowers_list,
                               most_popular_book_df=most_popular_book_df,
                               len=len
                               )
    elif request.values.get('submitGetPopularBook'):
        startDate=request.values.get('dateStart')
        endDate=request.values.get('dateEnd')
        startDate=convert_date(startDate)
        endDate=convert_date(endDate)
        books_list=most_popular_book(conn, startDate, endDate)
        print(books_list)
    return render_template('statistics.html',
                           most_popular_book_df=books_list,
                               borrowers_list=borrowers_list,
                               len=len)
