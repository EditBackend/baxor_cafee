from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["id", "name", "role", "password1", "password2", "face_password"]

    def validate(self, data):

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Parollar bir xil emas")

        if len(data["password1"]) != 4:
            raise serializers.ValidationError("Parol 4 xonali bo'lishi kerak")

        return data

    def create(self, validated_data):

        password = validated_data.pop("password1")
        validated_data.pop("password2")

        employee = Employee.objects.create(
            password=password,
            **validated_data
        )

        return employee