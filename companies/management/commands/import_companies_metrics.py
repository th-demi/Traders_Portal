import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from companies.models import Company, CompanyMetrics


class Command(BaseCommand):
    help = 'Import companies and company metrics from master.csv and metrics.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--master',
            type=str,
            default='master.csv',
            help='Path to master CSV file with companies data',
        )
        parser.add_argument(
            '--metrics',
            type=str,
            default='metrics.csv',
            help='Path to metrics CSV file',
        )

    def handle(self, *args, **options):
        master_path = options['master']
        metrics_path = options['metrics']

        self.stdout.write(f"Importing companies from {master_path} ...")

        try:
            with open(master_path, newline='', encoding='utf-8') as master_file:
                reader = csv.DictReader(master_file)
                existing_co_codes = set(
                    Company.objects.values_list('co_code', flat=True))

                companies_to_create = []
                for row in reader:
                    co_code = row['co_code']
                    if co_code not in existing_co_codes:
                        companies_to_create.append(
                            Company(
                                co_code=co_code,
                                company_name=row['name'],
                                symbol=row.get('symbol'),
                                scripcode=row.get('scripcode'),
                            )
                        )
                with transaction.atomic():
                    Company.objects.bulk_create(companies_to_create)
                self.stdout.write(self.style.SUCCESS(
                    f"Created {len(companies_to_create)} new companies."))

        except FileNotFoundError:
            raise CommandError(f"File {master_path} not found")

        self.stdout.write(f"Importing company metrics from {metrics_path} ...")

        try:
            with open(metrics_path, newline='', encoding='utf-8') as metrics_file:
                reader = csv.DictReader(metrics_file)
                # Fetch all companies keyed by co_code
                companies_dict = {c.co_code: c for c in Company.objects.all()}

                # Collect metrics to create and update separately
                metrics_to_create = []
                metrics_to_update = []

                # Fetch existing metrics to identify updates
                existing_metrics = CompanyMetrics.objects.select_related(
                    'company').all()
                metrics_by_co_code = {
                    m.company.co_code: m for m in existing_metrics}

                def parse_float(val):
                    try:
                        return float(val)
                    except (ValueError, TypeError):
                        return None

                for row in reader:
                    co_code = row['company_id']
                    pe = parse_float(row.get('pe'))
                    roe_ttm = parse_float(row.get('roe_ttm'))

                    company = companies_dict.get(co_code)
                    if not company:
                        self.stdout.write(self.style.WARNING(
                            f"Company with co_code {co_code} does not exist. Skipping."
                        ))
                        continue

                    existing_metric = metrics_by_co_code.get(co_code)
                    if existing_metric:
                        # Update existing metric object in memory
                        existing_metric.pe = pe
                        existing_metric.roe_ttm = roe_ttm
                        metrics_to_update.append(existing_metric)
                    else:
                        # Prepare new metric object
                        metrics_to_create.append(
                            CompanyMetrics(
                                company=company,
                                pe=pe,
                                roe_ttm=roe_ttm,
                            )
                        )

                with transaction.atomic():
                    if metrics_to_create:
                        CompanyMetrics.objects.bulk_create(metrics_to_create)
                    if metrics_to_update:
                        CompanyMetrics.objects.bulk_update(
                            metrics_to_update, ['pe', 'roe_ttm'])

                self.stdout.write(self.style.SUCCESS(
                    f"Created {len(metrics_to_create)} and updated {len(metrics_to_update)} company metrics."))

        except FileNotFoundError:
            raise CommandError(f"File {metrics_path} not found")
