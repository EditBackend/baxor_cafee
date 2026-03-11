from rest_framework import serializers
from .models import Organization


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"