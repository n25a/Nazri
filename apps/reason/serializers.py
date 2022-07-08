# Django libs
from rest_framework import serializers

# Internal libs
from .models import Reason


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'
