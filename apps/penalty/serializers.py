# Django libs
from rest_framework import serializers

# Internal libs
from .models import Penalty


class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = '__all__'


class PenaltyDeepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = [
            'level',
            'reason',
            'payed',
            'create_at',
            'modified_at',
        ]
        depth = 1
