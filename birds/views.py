from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.defaults import bad_request
from rest_condition import Or
from rest_framework import generics, viewsets, views, status, filters
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_rw_serializers.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from django.db.models import Q

from birds.models import Bird, Order, Family, Author, BirdImage, Image, Video, Audio
from birds.serializers import BirdSerializer, OrderSerializer, FamilySerializer, AuthorSerializer, AuthorIdsSerializer, \
    BirdReadSerializer, FamilyReadSerializer, AuthorMediaSerializer, BirdImageSerializer, ImageSerializer, \
    VideoSerializer, AudioSerializer, BirdImageReadSerializer, VideoReadSerializer, AudioReadSerializer
from birds.serializers import BirdIdsSerializer, OrderIdsSerializer, FamilyIdsSerializer
from users.permissions import AdminCustomPermission, EditorCustomPermission


class Birds(ListCreateAPIView):
    queryset = Bird.objects.all()
    write_serializer_class = BirdSerializer
    read_serializer_class = BirdReadSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )
    search_fields = ['scientific_names__name', 'common_names__name__text',
                     'family__scientific_names__name', 'family__order__scientific_names__name']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        queryset = Bird.objects.all()
        family_id = self.request.query_params.get('family', None)
        if family_id:
            queryset = queryset.filter(family=family_id)
        id_only = self.request.query_params.get('id_only', None)
        if id_only:
            self.read_serializer_class = BirdIdsSerializer
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            return super(ListCreateAPIView, self).create(request, *args, **kwargs)
        except IntegrityError as e:
            resp = {'detail': str(e)}
            return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleBird(RetrieveUpdateDestroyAPIView):
    queryset = Bird.objects.all()
    write_serializer_class = BirdSerializer
    read_serializer_class = BirdReadSerializer
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission), )

    def update(self, request, *args, **kwargs):
        try:
            return super(RetrieveUpdateDestroyAPIView, self).update(request, *args, **kwargs)
        except IntegrityError as e:
            resp = {'detail': str(e)}
            return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Images(CreateAPIView):
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class BirdImages(ListCreateAPIView):
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)
    parser_classes = [MultiPartParser, FormParser]
    write_serializer_class = BirdImageSerializer
    read_serializer_class = BirdImageReadSerializer
    queryset = BirdImage.objects.all()


class SingleBirdImage(RetrieveUpdateDestroyAPIView):
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)
    parser_classes = [MultiPartParser, FormParser]
    write_serializer_class = BirdImageSerializer
    read_serializer_class = BirdImageReadSerializer
    queryset = BirdImage.objects.all()


class Videos(ListCreateAPIView):
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)
    parser_classes = [MultiPartParser, FormParser]
    write_serializer_class = VideoSerializer
    read_serializer_class = VideoReadSerializer
    queryset = Video.objects.all()


class SingleVideo(RetrieveUpdateDestroyAPIView):
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)
    parser_classes = [MultiPartParser, FormParser]
    write_serializer_class = VideoSerializer
    read_serializer_class = VideoReadSerializer
    queryset = Video.objects.all()


class Audios(ListCreateAPIView):
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)
    parser_classes = [MultiPartParser, FormParser]
    write_serializer_class = AudioSerializer
    read_serializer_class = AudioReadSerializer
    queryset = Audio.objects.all()


class SingleAudio(RetrieveUpdateDestroyAPIView):
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)
    parser_classes = [MultiPartParser, FormParser]
    write_serializer_class = AudioSerializer
    read_serializer_class = AudioReadSerializer
    queryset = Audio.objects.all()


class Orders(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )
    search_fields = ['scientific_names__name']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        id_only = self.request.query_params.get('id_only', None)
        if id_only:
            self.serializer_class = OrderIdsSerializer
        return self.queryset


class SingleOrder(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AdminCustomPermission, )


class Families(ListCreateAPIView):
    queryset = Family.objects.all()
    write_serializer_class = FamilySerializer
    read_serializer_class = FamilyReadSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )
    search_fields = ['scientific_names__name']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        queryset = Family.objects.all()
        order_id = self.request.query_params.get('order', None)
        if order_id:
            queryset = queryset.filter(order=order_id)
        id_only = self.request.query_params.get('id_only', None)
        if id_only:
            self.read_serializer_class = OrderIdsSerializer
        return queryset


class SingleFamily(RetrieveUpdateDestroyAPIView):
    queryset = Family.objects.all()
    write_serializer_class = FamilySerializer
    read_serializer_class = FamilyReadSerializer
    permission_classes = (AdminCustomPermission, )


@api_view(['GET'])
def get_names(request):
    model = request.query_params.get('model', None)
    if model:
        if model == 'feeding':
            names = list(Bird.objects.order_by().values_list('feeding__names__text', flat=True).distinct())
        else:
            try:
                names = list(Bird.objects.order_by().values_list(model+'__name__text', flat=True).distinct())
            except Exception as e:
                resp = {
                    "message": str(e)
                }
                return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        if None in names:
            names.remove(None)
        resp = {
            "results": names
        }
        return Response(resp, status=status.HTTP_200_OK)
    else:
        resp = {
            "message": "model query param required"
        }
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class Authors(ListCreateAPIView):
    queryset = Author.objects.all()
    read_serializer_class = AuthorMediaSerializer
    write_serializer_class = AuthorSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission, )
    search_fields = ['first_name', 'last_name']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        queryset = Author.objects.filter(
            Q(images_authored__isnull=False) | Q(videos_authored__isnull=False) | Q(audios_authored__isnull=False)
        ).distinct()
        media_type = self.request.query_params.get('media_type', None)
        if media_type == 'images':
            queryset = Author.objects.filter(images_authored__isnull=False).distinct()
        elif media_type == 'videos':
            queryset = Author.objects.filter(videos_authored__isnull=False).distinct()
        elif media_type == 'audios':
            queryset = Author.objects.filter(audios_authored__isnull=False).distinct()
        id_only = self.request.query_params.get('id_only', None)
        if id_only:
            self.read_serializer_class = AuthorIdsSerializer
        return queryset


class SingleAuthor(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    read_serializer_class = AuthorMediaSerializer
    write_serializer_class = AuthorSerializer
    permission_classes = (AdminCustomPermission, )
