import time
import requests
from parsel import Selector
from tech_news.database import create_news


def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        pass
    return None


def scrape_updates(html_content):
    try:
        selector = Selector(text=html_content)
        news_urls = selector.css(".entry-title a::attr(href)").getall()
        return news_urls
    except Exception:
        return []


def scrape_next_page_link(html_content):
    try:
        selector = Selector(text=html_content)
        next_page_link = selector.css("a.next::attr(href)").get()
        return next_page_link
    except Exception:
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


def get_tech_news(amount):
    url = "https://blog.betrybe.com"
    links = []

    while amount > len(links):
        all_articles = fetch(url)
        links.extend(scrape_updates(all_articles))
        url = scrape_next_page_link(all_articles)

    links_content = []

    for link in links:
        links_content.append(scrape_news(fetch(link)))

    create_news(links_content[0:amount])

    return links_content[0:amount]
