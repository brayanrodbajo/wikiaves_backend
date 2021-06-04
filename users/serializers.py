from django.db import transaction
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from users.models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    def get_cleaned_data(self):
        validated_data = super(CustomRegisterSerializer, self).get_cleaned_data()
        validated_data.update({
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'role': self.validated_data.get('role', '')
        })
        return validated_data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.role = self.data.get('role')
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        exclude = ('reference', )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', None)
        instance.last_name = validated_data.get('last_name', None)
        instance.webpage = validated_data.get('webpage', None)
        instance.twitter = validated_data.get('twitter', None)
        instance.instagram = validated_data.get('instagram', None)
        instance.facebook = validated_data.get('facebook', None)
        instance.flicker = validated_data.get('flicker', None)
        instance.role = validated_data.get('role', None)
        return instance
