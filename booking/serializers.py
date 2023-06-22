from rest_framework import serializers


class ApplicationSerializer(serializers.Serializer): # noqa
    id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    number_persons = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()
    status = serializers.CharField(max_length=3)
    comment = serializers.CharField(max_length=128)
    client_name = serializers.CharField(max_length=64)
    client_phone = serializers.CharField(max_length=12)
    client_email = serializers.EmailField(max_length=32)
