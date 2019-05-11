from unittest.mock import patch

from django.utils import timezone
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from log import models as LogModels
from core.management.commands.seed import Command as SeedCommand


class CommandsTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when it is available."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.return_value = True
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 6)

    def test_seed(self):
        """Test the log is created"""
        call_command('seed')
        log = LogModels.Log.objects.all()

        self.assertEqual(log.count(), SeedCommand.COUNT)

    def test_refresh_log_level_count(self):
        """Test log_level_count view is refreshed"""
        LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.WARNING.value,
            message='Warning message body',
            details={
                'kwargs': {'k1': 'v1', 'k2': 'v2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )

        call_command('refresh_log_level_count')

        created_logs = LogModels.LogLevelCount.objects.all()

        self.assertEqual(len(created_logs), 1)
        self.assertEqual(
            created_logs[0].level,
            LogModels.LevelChoice.WARNING.value
        )

        LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.INFO.value,
            message='Info message body',
            details={
                'kwargs': {'k1': 'v1', 'k2': 'v2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )

        created_logs = LogModels.LogLevelCount.objects.all()
        self.assertEqual(len(created_logs), 1)

        call_command('refresh_log_level_count')

        created_logs = LogModels.LogLevelCount.objects.all()
        self.assertEqual(len(created_logs), 2)
