import pandas
def get_reader(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM reader
    ''', conn)


def get_book_reader(conn, reader_id):
 # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql('''
    WITH get_authors( book_id, authors_name)
    AS(
    SELECT book_id, GROUP_CONCAT(author_name)
    FROM author JOIN book_author USING(author_id)
    GROUP BY book_id
    )
    SELECT title AS Название, authors_name AS Авторы,
    borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
    book_reader_id
    FROM
    reader
    JOIN book_reader USING(reader_id)
    JOIN book USING(book_id)
    JOIN get_authors USING(book_id)
    WHERE reader.reader_id = :id
    ORDER BY 3
    ''', conn, params={"id": reader_id})
    return cur.lastrowid


# для обработки данных о взятой книге
def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    return True

def get_new_reader(conn, newReaderFio):
    cur = conn.cursor()
    cur.executescript(
    f'''
        INSERT INTO reader (reader_name)
        VALUES ('{newReaderFio}');
    ''')
    conn.commit()
    return pandas.read_sql('''SELECT MAX(reader_id) FROM reader LIMIT 1;''', conn).values[0][0];