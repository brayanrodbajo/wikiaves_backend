from django.contrib.auth.models import User
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
        bird = Bird.objects.get(id=id_bird)
        editor = CustomUser.objects.get(id=id_editor)
        BirdEditor.objects.create(bird=bird, editor=editor)
        response= {
            'status': 'assigned'
        }
        return Response(response, status=status.HTTP_200_OK)
