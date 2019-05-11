from rest_framework import viewsets, mixins

from log.models import LogLevelCount
from log import serializers


class LogViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Logs list, aggregated by type"""
    queryset = LogLevelCount.objects.all()
    serializer_class = serializers.LogLevelCountSerializer

    def get_queryset(self):
        """Return objects"""
        return self.queryset.order_by('-count')
