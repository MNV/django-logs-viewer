from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Refreshes the materialized view"""
    def handle(self, *args, **options):
        self.stdout.write('Materialized view refreshing...')
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW CONCURRENTLY log_level_count'
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Materialized view has been successfully refreshed!'
            )
        )
