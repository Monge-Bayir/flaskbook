import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: int, title: str, author: str) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT 
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]


def add_new_book(data):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO 'table_books' (title, author) VALUES (?, ?)
        """, data)


def search(author):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT * FROM 'table_books' WHERE author LIKE '%{author}%'
        """)
        return [Book(*row) for row in cursor.fetchall()]


def about(book_id):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS about (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                views INTEGER, 
                fk_about INTEGER REFERENCES table_books(id)
                )
        """)
        res = cursor.execute(f"SELECT * FROM about WHERE fk_about = {book_id}").fetchone()
        if res is not None:
            cursor.execute(f"""
                UPDATE about
                SET views = {res[2] + 1}
                WHERE fk_about = {book_id}
            """)

        return res


def get_all_abouts():
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM about")
        res = cursor.fetchall()
        return res