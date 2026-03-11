from rest_framework import serializers
from .models import KitchenTicket

class KitchenTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenTicket
        fields = "__all__"

class KitchenTicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenTicket
        fields = ['status']