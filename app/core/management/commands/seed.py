import random

from faker import Faker
from django.utils import timezone
from django.core.management.base import BaseCommand

from log.models import Log, LevelChoice


class Command(BaseCommand):
    """Populate the database with faked data"""
    help = 'Seed database for testing and development.'

    MODE_CLEAR = 'clear'
    MODE_REFRESH = 'refresh'
    COUNT = 20
    faker = None

    def __init__(self) -> None:
        super().__init__()
        self.faker = Faker()

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--mode',
            type=str,
            help='Mode'
        )
        parser.add_argument(
            '--count',
            type=int,
            help='Count',
            default=self.COUNT
        )

    def handle(self, *args, **options) -> None:
        """Handles the command"""
        self.stdout.write(self.style.WARNING('Seeding data...'))
        self.run_seed(options['mode'], options['count'])
        self.stdout.write(self.style.SUCCESS('Done.'))

    def clear_data(self) -> None:
        """Deletes all the table data"""
        self.stdout.write(self.style.WARNING('Delete log instances...'))
        Log.objects.all().delete()

    def create_log(self) -> None:
        """Creates a log object combining different elements from the list"""
        log = Log(
            time=timezone.now(),
            level=random.choice(list(LevelChoice)).value,
            message=self.faker.text(),
            details={
                'kwargs': {
                    'k1': self.faker.text()[:10],
                    'k2': self.faker.text()[:10]
                },
                'exec_time': timezone.now().isoformat(),
                'traceback': [
                    self.faker.text()[:100],
                    self.faker.text()[:100]
                ],
            }
        )

        log.save()
        self.stdout.write("'{}' log created".format(log))

    def run_seed(self, mode: str, count: int) -> None:
        """
        Seed the database.
        :param mode:
        :param count:
        :return:
        """
        if mode == self.MODE_CLEAR:
            self.clear_data()
            return

        self.stdout.write(self.style.WARNING('Creating logs...'))
        for i in range(count):
            self.stdout.write('№{}:'.format(i + 1))
            self.create_log()
