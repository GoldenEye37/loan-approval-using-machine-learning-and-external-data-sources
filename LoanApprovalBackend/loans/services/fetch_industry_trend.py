from datetime import datetime

from decouple import config
from loguru import logger
from serpapi import GoogleSearch
from textblob import TextBlob


def search_text(industry):
    # Industry search text
    industry_search_text = f"{industry} market trends in Zimbabwe"
    logger.info(f"Industry search text -> {industry_search_text}")
    return industry_search_text


def format_news_results(news_results):
    logger.info(f"News results -> {news_results}")

    formatted_industry_news = []
    logger.info(f"Formatting industry news.")
    for news_item in news_results:
        formatted_industry_news.append({
            'id': news_item.get('position', 'Unknown Position'),
            'title': news_item.get('title', 'Unknown Title'),
            'news_source': news_item.get('source', {}).get('name', 'Unknown Source'),
            'date_posted': news_item.get('date', 'Unknown Date')
        })
        logger.info(f"Successfully formatted industry news")
    return formatted_industry_news


def fetch_news_from_serpapi(industry):
    try:
        industry_results = {}
        logger.info(f"Inside fetch_news_from_serpapi function.")
        # setup params for search
        params = {
            "api_key": config("SERPAPI_API_KEY"),
            "engine": "google_news",
            "q": search_text(industry),
            "location": "Zimbabwe",
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "output": "json"}
        logger.info(f"Fetching industry news for {industry} from serpapi.")

        # fetch trends
        search = GoogleSearch(params)
        results = search.get_dict()
        logger.info(f"Results fetched successfully.")
        logger.info(f"Results -> {results}")

        news_results = results.get("news_results")

        # this creates a dictionary with the industry as the key and the news results as the value
        industry_results[industry] = format_news_results(news_results)
        logger.info(f"Industry news fetched successfully")
        return industry_results
    except Exception as e:
        logger.error(f"Error fetching industry trends -> {e}")
        return False


def get_current_year_news(industry_trends, current_year):
    #  initialize a dictionary
    industry_results_2024 = {}

    # get 2024 results only
    logger.info(f"Getting current year news.")
    for industry, news_items in industry_trends.items():
        news_items_2024 = [
            item for item in news_items if
            datetime.strptime(item['date_posted'], '%m/%d/%Y, %I:%M %p, %z UTC').year >= current_year
        ]

        industry_results_2024[industry] = news_items_2024
        logger.info(f"{industry} has: {len(news_items_2024)} counts")
    return industry_results_2024


def perform_sentiment_analysis(industry_news_2024):
    industry_sentiments = {}

    for industry, news_items in industry_news_2024.items():
        # Initialize variables to store overall sentiment polarity
        logger.info(f"Performing sentiment analysis for {industry}.")
        total_polarity = 0
        num_articles = len(news_items)

        # Perform sentiment analysis for each news item
        for news in news_items:
            news_heading = news["title"]
            news_polarity = TextBlob(news_heading).sentiment.polarity
            total_polarity += news_polarity

        # Calculate average polarity
        average_polarity = total_polarity / num_articles

        # Classify overall sentiment
        if average_polarity > 0:
            overall_sentiment = 'positive'
        elif average_polarity < 0:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'

        industry_sentiments[industry] = overall_sentiment
    # log sentiment analysis summary
    logger.info(f"Industry sentiment analysis -> {industry_sentiments}")
    return industry_sentiments


def fetch_industry_trends(industry):
    """
    The purpose of this function is to update industry trends in the database at a stipulated time.
    Fetch industry trends using SERPAPI and perform sentiment analysis using textblob.
    :param industry: industry name"""

    # fetch industry trends
    try:
        logger.info(f"Fetching industry trends invoked.")
        industry_trends = fetch_news_from_serpapi(industry)
        if industry_trends is False:
            return False
        # get current year news only
        current_year = datetime.now().year
        industry_news_2024 = get_current_year_news(industry_trends, current_year)

        # perform sentiment analysis on the news using textblob
        industry_sentiments = perform_sentiment_analysis(industry_news_2024)
        logger.info(f"Industry trends fetched successfully -> {industry_sentiments}")

        return industry_sentiments[industry]
    except Exception as e:
        logger.error(f"Error fetching industry trends -> {e}")
        return False
