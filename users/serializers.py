from django.db import transaction
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from users.models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    def get_cleaned_data(self):
        validated_data = super(CustomRegisterSerializer, self).get_cleaned_data()
        validated_data.update({
            'name': self.validated_data.get('name', ''),
            'role': self.validated_data.get('role', '')
        })
        return validated_data

    def save(self, request):
        user = super().save(request)
        user.name = self.data.get('name')
        user.role = self.data.get('role')
        user.save()
        return user

