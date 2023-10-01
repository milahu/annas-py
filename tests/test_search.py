from annas_py import search
from annas_py.models.args import FileType, Language, OrderBy
from annas_py.models.data import SearchResult

TEST_SEARCH_TERM = "Python"
LANGUAGE = Language.PT
FILE_TYPE = FileType.EPUB


def test_search():
    def check_instance(i):
        return isinstance(i, SearchResult)

    results = search(
        query=TEST_SEARCH_TERM,
        language=LANGUAGE,
        file_type=FILE_TYPE,
        order_by=OrderBy.NEWEST,
    )
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) == len(list(filter(check_instance, results)))
    assert f"[{LANGUAGE.value}]" in results[0].file_info.language
    assert results[0].file_info.extension == FILE_TYPE.value
