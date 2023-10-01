from html import unescape as html_unescape
from urllib.parse import urljoin

from bs4 import NavigableString

from ..models.args import FileType, Language, OrderBy
from ..models.data import SearchResult
from ..utils import html_parser
from . import BASE_URL
from .generic import extract_file_info, extract_publish_info


def search(
    query: str,
    language: Language = Language.ANY,
    file_type: FileType = FileType.ANY,
    order_by: OrderBy = OrderBy.MOST_RELEVANT,
) -> list[SearchResult]:
    if not query.strip():
        raise ValueError("query can not be empty")
    params = {
        "q": query,
        "lang": language.value,
        "ext": file_type.value,
        "sort": order_by.value,
    }
    soup = html_parser(urljoin(BASE_URL, "search"), params)
    raw_results = soup.find_all("a", class_="js-vim-focus")
    return list(filter(lambda i: i is not None, map(parse_result, raw_results)))


def parse_result(soup: NavigableString) -> SearchResult | None:
    def get_text(tag: str, cls: str = "") -> str:
        attrs = {"class": cls} if cls else {}
        return soup.find(tag, attrs=attrs).text

    try:
        title = get_text("h3").strip()
    except AttributeError:
        return None
    authors = get_text("div", "truncate italic")
    publisher, publish_date = extract_publish_info(get_text("div", "truncate text-sm"))
    file_info = extract_file_info(get_text("div", "truncate text-xs text-gray-500"))

    thumbnail = soup.find("img").get("src") or None
    id = soup.get("href").split("md5/")[-1]

    return SearchResult(
        id=id,
        title=html_unescape(title),
        authors=html_unescape(authors),
        file_info=file_info,
        thumbnail=thumbnail,
        publisher=html_unescape(publisher) if publisher else None,
        publish_date=publish_date,
    )
