from html import unescape as html_unescape
from urllib.parse import urljoin

from bs4 import Tag

from ..models.data import URL, Download
from ..utils import html_parser
from . import BASE_URL
from .generic import extract_file_info, extract_publish_info


def remove_search_icon(s: str) -> str:
    return s.replace("🔍", "").strip()


def get_informations(id: str) -> Download:
    soup = html_parser(urljoin(BASE_URL, f"md5/{id}"))

    title = remove_search_icon(soup.find("div", class_="text-3xl font-bold").text)
    authors = remove_search_icon(soup.find("div", class_="italic").text)
    description = soup.find(name="div", class_="js-md5-top-box-description").text
    thumbnail = soup.find("img").get("src") or None

    publish_info = soup.find("div", class_="text-md").text
    publisher, publish_date = extract_publish_info(publish_info)

    raw_file_info = soup.find("div", class_="text-sm text-gray-500").text
    file_info = extract_file_info(raw_file_info)

    download_links: list[URL] = []
    for container in soup.find_all("a", class_="js-download-link"):
        link = parse_link(container)
        if link is not None:
            download_links.append(link)

    return Download(
        title=html_unescape(title),
        description=html_unescape(description[1:-1]),
        authors=html_unescape(authors),
        file_info=file_info,
        urls=download_links,
        thumbnail=thumbnail,
        publisher=html_unescape(publisher) if publisher else None,
        publish_date=publish_date,
    )


def parse_link(link: Tag) -> URL | None:
    url = link.get("href")
    if url == "/datasets":
        return None
    if url[0] == "/":
        url = urljoin(BASE_URL, url[1:])
    return URL(html_unescape(link.text), url)
