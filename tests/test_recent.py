from annas_py import get_recent_downloads
from annas_py.models.data import RecentDownload


def test_recent_downloads():
    def check_instance(i):
        return isinstance(i, RecentDownload)
    books = get_recent_downloads()
    assert isinstance(books, list)
    assert len(books) > 0
    assert len(books) == len(list(filter(check_instance, books)))