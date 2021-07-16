import pytz
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, viewsets, views, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from birds.models import Bird
from users.models import CustomUser#, BirdEditor
from users.permissions import AdminCustomPermission
from users.serializers import UserProfileSerializer, PasswordResetSerializer, SetNewPasswordSerializer

from rest_auth.views import LoginView
from rest_auth.utils import jwt_encode
from rest_auth.models import TokenModel
from django.conf import settings

from .authentication import is_token_expired


def custom_create_token(token_model, user, serializer):
    token, created = token_model.objects.get_or_create(user=user)
    if not created:
        token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
        token.save()
    return token


class CustomLoginView(LoginView):
    def login(self):
        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = custom_create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        original_response = super().get_response()
        mydata = {"id": self.user.id, "role": self.user.role, "first_name": self.user.first_name,
                  "last_name": self.user.last_name, "username": self.user.username, "email": self.user.email,
                  "webpage": self.user.webpage, "twitter": self.user.twitter, "instagram": self.user.instagram,
                  "facebook": self.user.facebook, "flicker": self.user.flicker}
        original_response.data.update(mydata)
        return original_response


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AdminCustomPermission, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'url': serializer.validated_data['absurl']}, status=status.HTTP_200_OK)


class PasswordTokenCheckView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': False, 'msg': 'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'msg': 'Credentials valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            return Response({'success': False, 'msg': 'Token is not valid: '+str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'msg': 'Password reset success'}, status=status.HTTP_200_OK)


class Users(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AdminCustomPermission,)


class SingleUser(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

    def put(self, request, *args, **kwargs):
        self.queryset = CustomUser.objects.all()
        self.serializer_class = UserProfileSerializer
        self.permission_classes = (AdminCustomPermission,)
        return super().put(request, *args, **kwargs)


class BirdEditorView(APIView):
    permission_classes = (AdminCustomPermission, )

    def post(self, request):
        id_editor = request.data['editor']
        id_bird = request.data['bird']
        try:
            bird = Bird.objects.get(id=id_bird)
        except ObjectDoesNotExist:
            response = {
                'message': 'User not found',
                'success': False
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        try:
            editor = CustomUser.objects.get(id=id_editor)
        except ObjectDoesNotExist:
            response = {
                'message': 'Bird not found',
                'success': False
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        BirdEditor.objects.create(bird=bird, editor=editor)
        if editor.role != 'E':
            response = {
                'message': 'The user is not an editor',
                'success': False
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'message': 'Assigned',
                'success': True
            }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_token_status(request):
    if 'Authorization' in request.headers:
        try:
            key = request.headers['Authorization'].split(' ')[1]
            token = TokenModel.objects.get(key=key)
            if not is_token_expired(token):
                user = token.user
                resp = {"id": user.id, "role": user.role, "first_name": user.first_name,
                             "last_name": user.last_name, "username": user.username, "email": user.email,
                             "webpage": user.webpage, "twitter": user.twitter, "instagram": user.instagram,
                             "facebook": user.facebook, "flicker": user.flicker}
                return Response(resp, status=status.HTTP_200_OK)
            else:
                resp = {'detail': 'Token has expired'}
                return Response(resp, status=status.HTTP_401_UNAUTHORIZED)
        except IndexError as e:
            resp = {
                "message": "Authorization header should contain the word 'Token' followed by the key"
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resp = {
                "message": str(e)
            }
            return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        resp = {
            "message": "Authorization header required"
        }
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)
