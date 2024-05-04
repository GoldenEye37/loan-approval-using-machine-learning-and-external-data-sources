import logging

from celery import shared_task
from loguru import logger

from loans.models import Industry
from loans.services.fetch_industry_trend import fetch_industry_trends

# logger = logging.getLogger(__name__)


# create task to fetch industry trends
@shared_task
def fetch_and_update_industries_trends_task():
    """
    Fetch and update industry trends
    """
    try:
        logger.info(f"Task: Fetching industry trends from database.")
        industries = Industry.objects.all()

        # todo remove slicing
        logger.info(f"Task: sliced industries -> {industries[:1]}")
        for industry in industries[:1]:
            logger.info(f"Task: Industry -> {industry.name}")
            industry_trends = fetch_industry_trends(industry.name)
            if industry_trends is False:
                logger.error(f"Task: Error fetching industry trends -> {industry.name}")
                return False
            logger.info(f"Task: Fetched industry trends -> {industry_trends}")

            # update industry trends
            industry.trends = industry_trends
            industry.save()
            logger.info(f"Task: Updated industry trends -> {industry.name}, trend: {industry_trends}")
    except Exception as e:
        logger.error(f"Task: Error fetching industry trends -> {e}")
        return False
    return True


# create test task to test celery
@shared_task
def test_task():
    logger.info(f"Task: Adding task")  # Log the task result
    return 5 + 4
