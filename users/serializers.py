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
    webpage = serializers.URLField(required=False)
    twitter = serializers.URLField(required=False)
    instagram = serializers.URLField(required=False)
    facebook = serializers.URLField(required=False)
    flicker = serializers.URLField(required=False)
    id = serializers.IntegerField()

    class Meta:
        model = CustomUser
        exclude = ('reference', )

    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name', "")
        if first_name != "":
            instance.first_name = first_name
        last_name = validated_data.get('last_name', "")
        if last_name != "":
            instance.last_name = last_name
        webpage = validated_data.get('webpage', "")
        if webpage != "":
            instance.webpage = webpage
        twitter = validated_data.get('twitter', "")
        if twitter != "":
            instance.twitter = twitter
        instagram = validated_data.get('instagram', "")
        if instagram != "":
            instance.instagram = instagram
        facebook = validated_data.get('facebook', "")
        if facebook != "":
            instance.facebook = facebook
        flicker = validated_data.get('flicker', "")
        if flicker != "":
            instance.flicker = flicker
        role = validated_data.get('role', "")
        if role != "":
            instance.role = role
        instance.save()
        return instance
