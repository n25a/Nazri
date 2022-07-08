from rest_framework import serializers

from .models import CostumUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostumUser
        fields = [
            'id',
            'name',
            'mobile_number',
            'role',
            'rate',
        ]
