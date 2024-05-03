from django.core.management import BaseCommand

from loans.models import Industry


class Command(BaseCommand):
    help = 'Seeds the database with industries'

    def handle(self, *args, **options):
        industries = [
            'Agriculture, forestry, fishing, hunting',
            ' Mining, quarrying, oil and gas extraction',
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
            'Public adminstration']

        for industry in industries:
            Industry.objects.create(name=industry, trends='stable')

        self.stdout.write(self.style.SUCCESS('Industries seeded!'))
