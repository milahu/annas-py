from annas_py import search
from annas_py.models.args import FileType, Language, OrderBy
from annas_py.models.data import SearchResult

TEST_SEARCH_TERM = 'Python'

def test_search():
    def check_instance(i):
        return isinstance(i, SearchResult)
    results = search(
        query=TEST_SEARCH_TERM,
        language=Language.PT,
        file_type=FileType.EPUB,
        order_by=OrderBy.NEWEST
    )
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) == len(list(filter(check_instance, results)))
    assert results[0].file_info.language == Language.PT.value
    assert results[0].file_info.extension == Language.EPUB.value