from rest_framework import serializers

from .models import CostumUser


class CostumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostumUser
        fields = [
            "id",
            "name",
            "mobile_number",
            "role",
        ]


class CostumUserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostumUser
        fields = ["avatar"]
