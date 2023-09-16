from tech_news.database import find_news


def top_5_categories():
    news_data = find_news()

    categories_counter = {}

    for news in news_data:
        category = news["category"]
        if category in categories_counter:
            categories_counter[category] += 1
        else:
            categories_counter[category] = 1

    sorted_categories = sorted(
        categories_counter.items(), key=lambda x: (-x[1], x[0])
    )

    top_5 = [category for category, count in sorted_categories[:5]]

    return top_5
