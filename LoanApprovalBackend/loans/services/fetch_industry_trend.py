from decouple import config
from loguru import logger


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