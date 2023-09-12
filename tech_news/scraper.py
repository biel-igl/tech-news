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


# Requisito 3
def scrape_next_page_link(html_content):
    try:
        selector = Selector(text=html_content)
        # Encontre o link da próxima página usando um seletor CSS adequado
        next_page_link = selector.css("a.next::attr(href)").get()

        # Se encontrarmos o link da próxima página, retornamos a URL
        if next_page_link:
            return next_page_link
    except Exception:
        pass

    return None


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
