import requests
import time
from parsel import Selector
from tech_news.database import create_news


def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def scrape_updates(html_content):
    try:
        selector = Selector(text=html_content)
        news_urls = selector.css(".entry-title a::attr(href)").getall()
    except Exception:
        news_urls = []

    return news_urls


def scrape_next_page_link(html_content):
    try:
        selector = Selector(text=html_content)
        next_page_link = selector.css("a.next::attr(href)").get()

        if next_page_link:
            return next_page_link
    except Exception:
        pass

    return None


def scrape_news(html_content):
    selector = Selector(text=html_content)
    new_news = {
        "url": selector.css("link[rel=canonical]::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get().strip(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css("span.author a::text").get(),
        "reading_time": int(
            selector.css(".meta-reading-time::text").re_first(r"\d+")
        ),
        "summary": "".join(
            selector.css(".entry-content > p:first-of-type *::text").getall()
        ).strip(),
        "category": selector.css(".category-style span.label::text").get(),
    }

    return new_news


def fetch_news(url):
    html_content = fetch(url)
    if html_content is not None:
        return scrape_updates(html_content)
    return []


def fetch_and_store_news(url, n, news_list):
    html_content = fetch(url)

    if html_content is None:
        return n, False

    news_links = scrape_updates(html_content)[:n]

    for news_link in news_links:
        news_html = fetch(news_link)

        if news_html is not None:
            news_data = scrape_news(news_html)

            if news_data:
                create_news(news_data)
                news_list.append(news_data)
                n -= 1

    next_page_link = scrape_next_page_link(html_content)

    return n, next_page_link is None


def get_tech_news(n):
    news_list = []  # Lista para armazenar as notícias coletadas
    url = "https://blog.betrybe.com/page/1/"

    while n > 0:
        n, stop = fetch_and_store_news(url, n, news_list)

        if stop:
            break

        url = scrape_next_page_link(fetch(url))

    return news_list
