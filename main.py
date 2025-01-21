import json
import os

import pandas as pd

from otzaria.get_from_sefaria import Book
from otzaria.utils import sanitize_filename

new_books_file = "not_in_old.json"
with open(new_books_file, 'r', encoding='utf-8') as file:
    data = json.load(file)
lang = "hebrew"
for new_book in data:
    book_en_title = new_book["en_title"]
    book_he_title = new_book["he_title"]
    book_categories = new_book["path"]
    book = Book(book_en_title, lang=lang, he_title=book_he_title, categories=book_categories, get_links=True)
    file_name = sanitize_filename(book_he_title)
    file_path = list(map(lambda x: sanitize_filename(x), book_categories))
    file_path = os.path.join(*file_path, file_name)
    os.makedirs(file_path, exist_ok=True)
    book_file = os.path.join(file_path, file_name)
    book_content = book.process_book()
    book_refs = book.refs
    if book_content:
        with open(f"{book_file}.txt", "w", encoding="utf-8") as f:
            f.writelines(book_content)
        if book_refs:
            df = pd.DataFrame(book_refs)
            df.to_csv(f"{book_file}.csv", index=False)
        if book.links:
            with open(f'{book_file}.json', 'w', encoding='utf-8') as json_file:
                json.dump(book.links, json_file, indent=4, ensure_ascii=False)
