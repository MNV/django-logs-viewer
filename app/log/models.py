from django.contrib.postgres.fields import JSONField
from django.db import models
from enum import Enum


class LevelChoice(Enum):
    """Choices for log level field"""
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


class Log(models.Model):
    """Log entry model"""
    time = models.DateTimeField()
    level = models.CharField(
        max_length=20,
        choices=[(level, level.value) for level in LevelChoice]
    )
    message = models.CharField(max_length=500)
    details = JSONField()

    def __str__(self):
        return self.level


class LogLevelCount(models.Model):
    """Materialized view unmanaged model"""
    level = models.CharField(
        primary_key=True,
        max_length=20,
        choices=[(level, level.value) for level in LevelChoice]
    )
    count = models.IntegerField()

    class Meta:
        db_table = 'log_level_count'
        managed = False
