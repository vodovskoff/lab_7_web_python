import pandas
import sqlite3
import pandas as pd
def borrowers(conn, dateStart, dateEnd):
    return pd.read_sql(f'''
        SELECT distinct reader_name AS 'Имя_должника'
        FROM reader
        JOIN book_reader USING (reader_id)
        WHERE borrow_date>{dateStart} and return_date IS NULL 
    ''', conn)

def most_popular_book(conn, dateStart, dateEnd):
    print(dateStart)
    print(dateEnd)
    return pd.read_sql(f'''
        SELECT title AS 'Название', count(book_reader_id) as 'Количество'
        FROM book
        JOIN book_reader ON (book.book_id = book_reader.book_id)
        WHERE book_reader.borrow_date>='{dateStart}' and book_reader.borrow_date<='{dateEnd}'
        GROUP BY book_reader.book_id
        HAVING count(book_reader_id)=(
            SELECT count(book_reader_id)
            FROM book
            JOIN book_reader ON (book.book_id = book_reader.book_id)
            WHERE book_reader.borrow_date>='{dateStart}' and book_reader.borrow_date<='{dateEnd}'
            GROUP BY book_reader.book_id
            ORDER BY count(book_reader_id) desc limit 1
             )
    ''', conn)
