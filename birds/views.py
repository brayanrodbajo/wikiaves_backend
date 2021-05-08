from django.contrib.auth.models import User
from rest_condition import Or
from rest_framework import generics, viewsets, views, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from birds.models import Bird, Order, Family
from birds.serializers import BirdSerializer, OrderSerializer, FamilySerializer
from users.permissions import AdminCustomPermission, EditorCustomPermission


class Birds(ListCreateAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )

    def get_queryset(self):
        queryset = Bird.objects.all()
        family_id = self.request.query_params.get('family', None)
        if family_id:
            queryset = queryset.filter(family=family_id)
        return queryset


class SingleBird(RetrieveUpdateDestroyAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission), )


class Orders(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )


class SingleOrder(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AdminCustomPermission, )


class Families(ListCreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )

    def get_queryset(self):
        queryset = Family.objects.all()
        order_id = self.request.query_params.get('order', None)
        if order_id:
            queryset = queryset.filter(order=order_id)
        return queryset


class SingleFamily(RetrieveUpdateDestroyAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = (AdminCustomPermission, )

