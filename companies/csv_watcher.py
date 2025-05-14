import time
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.core.management.base import BaseCommand
from django.conf import settings
from companies.models import Company

CSV_DIR = os.path.join(os.path.dirname(__file__), 'csv_uploads')

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.csv'):
            return
        self.process(event.src_path)

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.csv'):
            return
        self.process(event.src_path)

    def process(self, file_path):
        print(f"Processing CSV: {file_path}")
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            company_name = row.get('company_name')
            symbol = row.get('symbol') if not pd.isna(row.get('symbol')) else None
            scripcode = str(int(row.get('scripcode'))) if not pd.isna(row.get('scripcode')) else None
            if company_name:
                Company.objects.update_or_create(
                    company_name=company_name,
                    defaults={'symbol': symbol, 'scripcode': scripcode}
                )

if __name__ == "__main__":
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, path=CSV_DIR, recursive=False)
    print(f"Watching directory: {CSV_DIR}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 