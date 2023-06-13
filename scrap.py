import asyncio
import json
import re
import aiohttp
from bs4 import BeautifulSoup


async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_author(session, author_url):
    author_info_html = await fetch_html(session, author_url)
    author_info_soup = BeautifulSoup(author_info_html, "lxml")
    author_fullname = author_info_soup.select_one(".author-title").get_text(strip=True).replace("-", " ")
    born_date = author_info_soup.select_one(".author-born-date").get_text(strip=True)
    born_location = author_info_soup.select_one(".author-born-location").get_text(
        strip=True
    )
    description = re.sub(
        r'"',
        "",
        author_info_soup.select_one(".author-description").get_text(strip=True),
    )

    return {
        "fullname": author_fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }


def parse_quote(quote_element):
    quote_text = (
        quote_element.select_one(".text")
        .get_text(strip=True)
        .replace("\u201c", "")
        .replace("\u201d", "")
    )
    author = quote_element.select_one(".author").get_text(strip=True)
    tags = [tag.text for tag in quote_element.select(".tags .tag")]

    return {
        "quote": quote_text,
        "author": author,
        "tags": tags,
    }


async def get_quotes(session, url):
    html = await fetch_html(session, url)
    soup_quotes = BeautifulSoup(html, "lxml").select(".quote")
    quotes = [parse_quote(quote_element) for quote_element in soup_quotes]
    author_links = {
        quote_element.select_one("a")["href"] for quote_element in soup_quotes
    }

    return quotes, author_links


async def get_authors(session, base_url, author_links):
    authors = []

    for author_link in author_links:
        author_url = base_url + author_link
        author = await parse_author(session, author_url)
        authors.append(author)

    return authors


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


async def main(num_pages):

    base_url = "http://quotes.toscrape.com"

    all_quotes = []
    all_authors = set()

    async with aiohttp.ClientSession() as session:

        for page in range(1, num_pages + 1):

            page_url = f"/page/{page}"
            url = base_url + page_url

            quotes, author_links = await get_quotes(session, url)
            all_quotes.extend(quotes)

            # Додає унікальні посилання
            all_authors.update(author_links)

            # перевірка на існування сторінок
            response = await fetch_html(session, url)
            soup = BeautifulSoup(response, 'lxml')
            if not len(soup.select('.next')):
                break

        authors = []
        for author_link in all_authors:
            author_url = base_url + author_link
            author = await parse_author(session, author_url)
            authors.append(author)

    save_to_json(all_quotes, "quotes.json")
    save_to_json(authors, "authors.json")


if __name__ == "__main__":
    asyncio.run(main(10))
