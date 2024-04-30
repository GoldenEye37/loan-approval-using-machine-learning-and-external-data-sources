from datetime import datetime

from decouple import config
from loguru import logger
from serpapi import GoogleSearch


def search_text(industry):
    # Industries
    industries = ['Agriculture, forestry, fishing, hunting',
                  'Mining, quarrying, oil and gas extraction',
                  'Utilities',
                  'Construction',
                  'Manufacturing',
                  'Wholesale_trade',
                  'Retail_trade',
                  'Transportation, warehousing',
                  'Information',
                  'Finance, Insurance',
                  'Real estate, rental, leasing',
                  'Professional, scientific, technical services',
                  'Management of companies, enterprises',
                  'Administrative support, waste management',
                  'Educational',
                  'Healthcare, Social_assist',
                  'Arts, Entertain, recreation',
                  'Accomodation, Food services',
                  'Other services',
                  'Public adminstration'
                  ]

    industry_search_text = {industry: f"{industry} market trends in Zimbabwe" for industry in industries}
    print(industry_search_text)


def format_news_results(news_results):
    formatted_industry_news = []

    for news_item in news_results:
        formatted_industry_news.append({
            'id': news_item.get('position', 'Unknown Position'),
            'title': news_item.get('title', 'Unknown Title'),
            'news_source': news_item.get('source', {}).get('name', 'Unknown Source'),
            'date_posted': news_item.get('date', 'Unknown Date')
        })
        logger.info(f"Formatted industry news")
    return formatted_industry_news


def fetch_trends(industry):
    try:
        industry_results = {}

        # setup params for search
        params = {
            "api_key": config("SERPAPI_API_KEY"),
            "engine": "google",
            "q": search_text(industry),
            "location": "Zimbabwe",
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "output": "json"}
        logger.info(f"Fetching industry trends for {industry} -> {params}")

        # fetch trends
        search = GoogleSearch(params)
        results = search.get_dict()
        logger.info(f"Industry trends fetched successfully -> {results}")

        news_results = results.get("news_results")

        # this creates a dictionary with the industry as the key and the news results as the value
        industry_results[industry] = format_news_results(news_results)
        return industry_results
    except Exception as e:
        logger.error(f"Error fetching industry trends -> {e}")
        return False


def get_current_year_news(industry_trends, current_year):
    #  initialize a dictionary
    industry_results_2024 = {}

    # get 2024 results only
    for industry, news_items in industry_trends.items():
        news_items_2024 = [
            item for item in news_items if
            datetime.strptime(item['date_posted'], '%m/%d/%Y, %I:%M %p, %z UTC').year >= current_year
        ]

        industry_results_2024[industry] = news_items_2024
        logger.info(f"{industry}: {len(news_items_2024)} counts")
    return industry_results_2024


def fetch_industry_trends(industry):
    """Fetch industry trends using SERPAI and perform sentiment analysis using textblob."""
    # fetch industry trends
    try:
        industry_trends = fetch_trends(industry)
        # get current year news only
        current_year = datetime.now().year
        current_year_news = get_current_year_news(industry_trends, current_year)
    except Exception as e:
        logger.error(f"Error fetching industry trends -> {e}")
        return False
