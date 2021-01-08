from django.contrib.auth.models import User
from rest_condition import Or
from rest_framework import generics, viewsets, views, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from birds.models import Bird
from birds.serializers import BirdSerializer
from users.permissions import AdminCustomPermission, EditorCustomPermission


class Birds(ListCreateAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )


class SingleBird(RetrieveUpdateDestroyAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission), )
