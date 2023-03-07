from rest_framework import serializers
from .models import Bus

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"

class BusSerializerWithDistance(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(required=False)
    class Meta:
        model = Bus
        fields = "__all__"

    def get_distance(self, obj):
        return obj.distance.m