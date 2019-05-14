import json

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from log.serializers import SearchByBodySerializer
from log import models as LogModels

LOG_LIST_URL = reverse('log:search-by-field-list')


class SearchByFieldApiTests(TestCase):
    """Test the search by field API endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_details_field(self):
        """Test searching logs by details field value"""
        info_log = LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.INFO.value,
            message='Info message body',
            details={
                'kwargs': {'k': 'v'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line11', 'line22'],
            }
        )
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
        critical_log_exec_time = timezone.now().isoformat()
        critical_log = LogModels.Log.objects.create(
            time=timezone.now(),
            level=LogModels.LevelChoice.CRITICAL.value,
            message='Critical message body',
            details={
                'kwargs': {'q1': 'c1', 'q2': 'c2'},
                'exec_time': critical_log_exec_time,
                'traceback': 'traceback search text',
            }
        )

        info_log_serializer = SearchByBodySerializer(info_log)
        warning_log_serializer = SearchByBodySerializer(warning_log)
        critical_log_serializer = SearchByBodySerializer(critical_log)

        # kwargs
        res = self.client.get(
            LOG_LIST_URL,
            {'kwargs': json.dumps({'q1': 'c1'})}
        )
        self.assertNotIn(info_log_serializer.data, res.data['results'])
        self.assertIn(critical_log_serializer.data, res.data['results'])

        # exec_time
        res = self.client.get(
            LOG_LIST_URL,
            {'exec_time': '{}'.format(critical_log_exec_time)}
        )
        self.assertNotIn(info_log_serializer.data, res.data['results'])
        self.assertIn(critical_log_serializer.data, res.data['results'])

        # traceback
        res = self.client.get(
            LOG_LIST_URL,
            {'traceback': '{}'.format('traceback search text')}
        )
        self.assertNotIn(info_log_serializer.data, res.data['results'])
        self.assertIn(critical_log_serializer.data, res.data['results'])

        res = self.client.get(
            LOG_LIST_URL,
            {'traceback': ['line11', 'line22']}
        )
        self.assertIn(info_log_serializer.data, res.data['results'])
        self.assertNotIn(warning_log_serializer.data, res.data['results'])
        self.assertNotIn(critical_log_serializer.data, res.data['results'])

        res = self.client.get(
            LOG_LIST_URL,
            {'traceback': ['line1', 'line2']}
        )

        self.assertIn(warning_log_serializer.data, res.data['results'])
        self.assertNotIn(info_log_serializer.data, res.data['results'])
        self.assertNotIn(critical_log_serializer.data, res.data['results'])
