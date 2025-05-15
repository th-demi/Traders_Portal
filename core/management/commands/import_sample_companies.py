from django.core.management.base import BaseCommand
from companies.models import Company


class Command(BaseCommand):
    help = 'Import sample company data for testing'

    def handle(self, *args, **kwargs):
        # Check if we already have companies
        if Company.objects.exists():
            self.stdout.write(self.style.WARNING(
                'Companies already exist. Skipping import.'))
            return

        # Sample company data
        sample_companies = [
            {'company_name': 'Apple Inc.', 'symbol': 'AAPL', 'scripcode': '123456'},
            {'company_name': 'Microsoft Corporation',
                'symbol': 'MSFT', 'scripcode': '234567'},
            {'company_name': 'Amazon.com Inc.',
                'symbol': 'AMZN', 'scripcode': '345678'},
            {'company_name': 'Alphabet Inc.',
                'symbol': 'GOOGL', 'scripcode': '456789'},
            {'company_name': 'Facebook Inc.', 'symbol': 'FB', 'scripcode': '567890'},
            {'company_name': 'Tesla, Inc.', 'symbol': 'TSLA', 'scripcode': '678901'},
            {'company_name': 'NVIDIA Corporation',
                'symbol': 'NVDA', 'scripcode': '789012'},
            {'company_name': 'Berkshire Hathaway Inc.',
                'symbol': 'BRK.A', 'scripcode': '890123'},
            {'company_name': 'Johnson & Johnson',
                'symbol': 'JNJ', 'scripcode': '901234'},
            {'company_name': 'JPMorgan Chase & Co.',
                'symbol': 'JPM', 'scripcode': '012345'},
            {'company_name': 'Visa Inc.', 'symbol': 'V', 'scripcode': '123450'},
            {'company_name': 'Walmart Inc.', 'symbol': 'WMT', 'scripcode': '234561'},
            {'company_name': 'Mastercard Incorporated',
                'symbol': 'MA', 'scripcode': '345672'},
            {'company_name': 'Procter & Gamble Co.',
                'symbol': 'PG', 'scripcode': '456783'},
            {'company_name': 'UnitedHealth Group Incorporated',
                'symbol': 'UNH', 'scripcode': '567894'},
            {'company_name': 'Home Depot, Inc.',
                'symbol': 'HD', 'scripcode': '678905'},
            {'company_name': 'Bank of America Corporation',
                'symbol': 'BAC', 'scripcode': '789016'},
            {'company_name': 'Intel Corporation',
                'symbol': 'INTC', 'scripcode': '890127'},
            {'company_name': 'Verizon Communications Inc.',
                'symbol': 'VZ', 'scripcode': '901238'},
            {'company_name': 'AT&T Inc.', 'symbol': 'T', 'scripcode': '012349'},
        ]

        # Create company objects
        companies = [Company(**data) for data in sample_companies]
        Company.objects.bulk_create(companies)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {len(companies)} sample companies.'))
