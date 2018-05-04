from rest_framework import serializers


class LEDRGBSerializer(serializers.Serializer):

    red = serializers.IntegerField(min_value=0, max_value=255)
    green = serializers.IntegerField(min_value=0, max_value=255)
    blue = serializers.IntegerField(min_value=0, max_value=255)
