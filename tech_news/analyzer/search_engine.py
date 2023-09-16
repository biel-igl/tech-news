from datetime import datetime
from tech_news.database import db


def search_by_title(title: str):
    lower_title = title.lower()
    result = db.news.find(
        {"title": {"$regex": f".*{lower_title}.*", "$options": "i"}},
        {"title": 1, "url": 1},
    )

    return [(news["title"], news["url"]) for news in result]


def search_by_date(date_str: str):
    try:
        search_date = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = search_date.strftime("%d/%m/%Y")

        result = db.news.find(
            {"timestamp": formatted_date}, {"title": 1, "url": 1}
        )

        return [(news["title"], news["url"]) for news in result]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
