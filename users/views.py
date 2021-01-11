from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, viewsets, views, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from birds.models import Bird
from users.models import CustomUser, BirdEditor
from users.permissions import AdminCustomPermission
from users.serializers import CustomRegisterSerializer


# ViewSets define the view behavior.
class Users(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomRegisterSerializer


class SingleUser(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomRegisterSerializer


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
