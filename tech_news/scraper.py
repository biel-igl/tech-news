import requests
import time
from parsel import Selector


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


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
