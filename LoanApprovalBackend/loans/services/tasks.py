from celery import shared_task
from loguru import logger

from loans.models import Industry
from loans.services.fetch_industry_trend import fetch_industry_trends


# create task to fetch industry trends
@shared_task(bind=True, name='fetch_industry_trends')
def fetch_and_update_industries_trends_task(self):
    """
    Fetch and update industry trends
    :param self:
    :return:
    """

    try:
        logger.info(f"Task: Fetching industry trends")
        industries = Industry.objects.all()

        # todo remove slicing
        for industry in industries[:1]:
            industry_trends = fetch_industry_trends(industry.name)
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
@shared_task(bind=True, name='test_task')
def test_task(self):
    logger.info(f"Task: Testing task")
    return True
