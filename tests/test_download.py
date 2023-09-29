import annas_py

TEST_BOOK_ID = '7137f16be1acec896b36ff695fff82dc'

def test_download():
    book = annas_py.get_information(TEST_BOOK_ID)
    assert book is not None and isinstance(book, annas_py.models.data.Download)