import pandas
import sqlite3
def return_book(conn, reader_book_id):
    cur = conn.cursor()

    cur.executescript(f'''
    UPDATE book
    SET available_numbers = available_numbers + 1
    WHERE book_id = (SELECT book_id FROM book_reader WHERE return_date IS NULL and book_reader_id = {reader_book_id});
    
    UPDATE book_reader
    SET return_date = DATE()
    WHERE book_reader_id = {reader_book_id}
        ''')

    return conn.commit()