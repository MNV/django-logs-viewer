from django.utils import timezone
from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from log.serializers import LogLevelCountSerializer
from log import models as LogModels

LOG_LEVEL_COUNT_URL = reverse('log:loglevelcount-list')


class PrivateTagsApiTests(TestCase):
    """Test the count by types API endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags(self):
        """Test retrieving logs"""
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
        call_command('refresh_log_level_count')

        res = self.client.get(LOG_LEVEL_COUNT_URL)

        tags = LogModels.LogLevelCount.objects.all().order_by('-count')
        serializer = LogLevelCountSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': serializer.data,
        }
        self.assertEqual(res.data, serializer_data)
