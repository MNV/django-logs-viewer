from rest_framework import serializers

from log.models import LogLevelCount


class LogLevelCountSerializer(serializers.ModelSerializer):
    """Serializer for LogLevelCount object"""

    class Meta:
        model = LogLevelCount
        fields = ('level', 'count')
        read_only_Fields = ('level', 'count')
