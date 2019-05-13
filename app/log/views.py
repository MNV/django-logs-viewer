from rest_framework import viewsets, mixins, filters

from log.models import Log, LogLevelCount
from log import serializers


class CountByTypesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Logs list, aggregated by type"""
    queryset = LogLevelCount.objects.all()
    serializer_class = serializers.LogLevelCountSerializer

    def get_queryset(self):
        """Return objects"""
        return self.queryset.order_by('-count')


class SearchByBodyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Search logs by message body using full-text index"""
    queryset = Log.objects.all()
    serializer_class = serializers.SearchByBodySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('@message',)

    def get_queryset(self):
        """Return objects"""
        return self.queryset.order_by('-id')
