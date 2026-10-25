import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path



class Book:
    book_database = "database/books.json"
    book_data = []
    try:
        if Path(book_database).exists():
            with open(book_database) as fs:
                book_data = json.loads(fs.read())
        else:
            print("No such data found!")
    except Exception as err:
        print(f"An error occurred as {err}")

    @classmethod
    def __update(cls):
        with open(cls.book_database, "w") as fs:
            fs.write(json.dumps(Book.book_data, indent=4))

    @classmethod
    def __unique_bookid(cls):
        while True:
            alpha = random.choices(string.ascii_letters, k=3)
            nums = random.choices(string.digits, k=10)

            id = alpha + nums
            random.shuffle(id)
            new_id = "BOOK." + "".join(id)
            idcheck = [i for i in Book.book_data if i["Book-ID"] == new_id]
            if len(idcheck) > 0:
                continue
            return new_id

    @classmethod
    def uniquebook_id(cls):
        return cls.__unique_bookid()

    @classmethod
    def update(cls):
        return cls.__update()

    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category
        self.book_id = Book.uniquebook_id()
        self.status = "Available"

        book_info = {
            "Title": self.title,
            "Author": self.author,
            "Category": self.category,
            "Book-ID": self.book_id,
            "Status": self.status,
        }
        Book.book_data.append(book_info)
        Book.update()
