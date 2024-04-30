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
    return formatted_industry_news

def fetch_trends(industry):
    try:
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
        # fetch trends
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results.get("news_results")
        
        format_results = format_news_results(news_results)
    except Exception as e:
        logger.error(f"Error fetching industry trends -> {e}")
        return False


def fetch_industry_trends(industry):
    """Fetch industry trends using SERPAI and perform sentiment analysis using textblob."""
    # fetch industry trends
    try:
        industry_trends = fetch_trends(industry)
    except Exception as e:
        logger.error(f"Error fetching industry trends -> {e}")
        return False