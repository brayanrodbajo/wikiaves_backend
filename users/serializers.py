from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed

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
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    webpage = serializers.URLField(required=False)
    twitter = serializers.URLField(required=False)
    instagram = serializers.URLField(required=False)
    facebook = serializers.URLField(required=False)
    flicker = serializers.URLField(required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CustomUser
        exclude = ('reference', 'password')

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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError('Error')
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Invalid e-mail address')
        return value

    def validate(self, attrs):
        email = attrs['email']
        if self.validate_email(email):
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context['request']
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
            attrs['absurl'] = absurl
            return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


from birds.serializers import BirdSerializer
from birds.models import Bird


class UserProfileBirdsReadSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    webpage = serializers.URLField(required=False)
    twitter = serializers.URLField(required=False)
    instagram = serializers.URLField(required=False)
    facebook = serializers.URLField(required=False)
    flicker = serializers.URLField(required=False)
    id = serializers.IntegerField(required=False)
    birds_assigned = BirdSerializer(many=True, required=False, allow_null=True, read_only=True)

    class Meta:
        model = CustomUser
        exclude = ('reference', 'password')


class UserProfileBirdsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    webpage = serializers.URLField(required=False)
    twitter = serializers.URLField(required=False)
    instagram = serializers.URLField(required=False)
    facebook = serializers.URLField(required=False)
    flicker = serializers.URLField(required=False)
    id = serializers.IntegerField(required=False)
    birds_assigned = serializers.PrimaryKeyRelatedField(queryset=Bird.objects.all(), many=True,
                                                        required=False, allow_null=True)

    class Meta:
        model = CustomUser
        exclude = ('reference', 'password')

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
        birds_assigned = validated_data.get('birds_assigned', "")
        if birds_assigned != "":
            for bird in birds_assigned:
                bird.current_editor = instance
                bird.save()
        instance.save()
        return instance