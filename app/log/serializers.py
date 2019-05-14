from rest_framework import serializers

from log.models import Log, LogLevelCount


class LogLevelCountSerializer(serializers.ModelSerializer):
    """Serializer for LogLevelCount object"""

    class Meta:
        model = LogLevelCount
        fields = ('level', 'count')
        read_only_Fields = ('level', 'count')


class SearchByBodySerializer(serializers.ModelSerializer):
    """Serializer for SearchByBody object"""

    class Meta:
        model = Log
        fields = ('id', 'time', 'level', 'message', 'details')
        read_only_Fields = ('id', 'time', 'level', 'message', 'details')


class SearchByFieldSerializer(serializers.ModelSerializer):
    """Serializer for SearchByBody object"""

    class Meta:
        model = Log
        fields = ('id', 'time', 'level', 'message', 'details')
        read_only_Fields = ('id', 'time', 'level', 'message', 'details')
