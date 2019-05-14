from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from log.serializers import SearchByBodySerializer
from log import models as LogModels

LOG_LIST_URL = reverse('log:search-by-body-list')


class SearchByBodyApiTests(TestCase):
    """Test the search by body API endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        """Test retrieving a list of logs"""
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

        res = self.client.get(LOG_LIST_URL)

        logs = LogModels.Log.objects.all().order_by('-id')
        serializer = SearchByBodySerializer(logs, many=True)

        serializer_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': serializer.data,
        }
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer_data)

    def test_search(self):
        """Test full text logs search"""
        warning_log = LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.WARNING.value,
            message='Warning message body',
            details={
                'kwargs': {'k1': 'v1', 'k2': 'v2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )
        info_log = LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.INFO.value,
            message='Info message body',
            details={
                'kwargs': {'k1': 'v1', 'k2': 'v2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )
        critical_log = LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.CRITICAL.value,
            message='Critical message body',
            details={
                'kwargs': {'k1': 'v1', 'k2': 'v2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )

        res = self.client.get(
            LOG_LIST_URL,
            {'search': '{}'.format('info')}
        )

        info_log_serializer = SearchByBodySerializer(info_log)
        warning_log_serializer = SearchByBodySerializer(warning_log)
        critical_log_serializer = SearchByBodySerializer(critical_log)

        self.assertIn(info_log_serializer.data, res.data['results'])
        self.assertNotIn(critical_log_serializer.data, res.data['results'])

        res = self.client.get(
            LOG_LIST_URL,
            {'search': '{}'.format('messages')}
        )

        self.assertIn(info_log_serializer.data, res.data['results'])
        self.assertIn(warning_log_serializer.data, res.data['results'])
