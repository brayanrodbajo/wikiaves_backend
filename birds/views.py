from django.contrib.auth.models import User
from rest_framework import generics, viewsets, views

from users.models import CustomUser
from users.serializers import UserSerializer


# ViewSets define the view behavior.
class UserViewSet(views.APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
