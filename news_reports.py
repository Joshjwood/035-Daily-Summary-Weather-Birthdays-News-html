import requests
import datetime
from privates import *

YESTERDAY = datetime.timedelta(days=1)

NEWS_API = NEWS_API
NEWS_ENDPOINT = NEWS_ENDPOINT

#takes news data from the functions below and formats it with some HTML into a news block
def news_block(news_data, source):
    report = source
    #print(news_data)
    for i in range(0, 3):
        link_text = news_data["articles"][i]["url"]
        image_ref = news_data["articles"][i]["urlToImage"]
        report += f'<a href="{link_text}"><img src="{image_ref}" alt="ALT TEXT"></a><br>'
        report += "<strong>" + news_data["articles"][i]["title"] + "</strong><br>"
        report += news_data["articles"][i]["description"]
        report += "<br><br><br>"
    return report

def bbc_today():
    news_params = {
        "apiKey": NEWS_API,
        "sources": "bbc-news",
        "sortBy": "popularity",
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    ###########################
    source = f'<strong>{news_data["articles"][0]["source"]["name"]}</strong>:<br>'
    return news_block(news_data, source)

def reuters_today():
    news_params = {
        "apiKey": NEWS_API,
        "sources": "reuters",
        "sortBy": "popularity",
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    ###########################
    source = f'<strong>{news_data["articles"][0]["source"]["name"]}</strong>:<br>'
    return news_block(news_data, source)

def guardian_today():
    news_params = {
        "apiKey": NEWS_API,
        "sources": "the-verge",
        "sortBy": "popularity",
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    ###########################
    source = f'<strong>{news_data["articles"][0]["source"]["name"]}</strong>:<br>'
    return news_block(news_data, source)

def yesterday_top_3():
    news_params = {
        "apiKey": NEWS_API,
        "country": "gb",
        # "qInTitle": COMPANY_NAME,
        "from": YESTERDAY,
        "sortBy": "popularity",
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    ###########################
    source = f'<strong>Top 3 stories from Yesterday</strong>:<br>'
    try:
        report = news_block(news_data, source)
        return report
    except:
        return "Failed to recall yesterdays news"