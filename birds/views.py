import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
import django_filters.rest_framework
from django.views.defaults import bad_request
from rest_condition import Or
from rest_framework import generics, viewsets, views, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_rw_serializers.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from django.db.models import Q

from birds.models import Bird, Order, Family, BirdImage, Image, Video, Audio, Location, MultimediaAuthor
from birds.serializers import BirdSerializer, OrderSerializer, FamilySerializer, \
    BirdReadSerializer, FamilyReadSerializer, BirdImageSerializer, ImageSerializer, \
    VideoSerializer, AudioSerializer, BirdImageReadSerializer, VideoReadSerializer, AudioReadSerializer, \
    AuthorSerializer, AuthorIdsSerializer, AuthorMediaSerializer
from birds.serializers import BirdIdsSerializer, OrderIdsSerializer, FamilyIdsSerializer
from users.permissions import AdminCustomPermission, EditorCustomPermission


from services.doc_to_model import bird_exists, handle_uploaded_file, delete_uploaded_file, doc_to_model


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        exact = request.query_params.get('exact', None)
        search_fields = request.GET.getlist('search_fields', [])
        default_s_f = super(DynamicSearchFilter, self).get_search_fields(view, request)
        if len(search_fields) > 0:
            return search_fields
        elif exact:
            return ['='+s_f for s_f in default_s_f]
        return default_s_f


class Birds(ListCreateAPIView):
    queryset = Bird.objects.all()
    write_serializer_class = BirdSerializer
    read_serializer_class = BirdReadSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission,)
    filter_backends = [DynamicSearchFilter, django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['scientific_names__name', 'common_names__name__text',
                     'family__scientific_names__name', 'family__order__scientific_names__name']
    filterset_fields = ['id', 'draft', 'scientific_names__name', 'common_names__name__text',
                        'family__scientific_names__name', 'family__order__scientific_names__name']
    ordering_fields = '__all__'

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
    permission_classes = (Or(AdminCustomPermission, EditorCustomPermission),)

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
    permission_classes = (AdminCustomPermission,)
    search_fields = ['scientific_names__name']
    filterset_fields = ['scientific_names__name']
    ordering_fields = '__all__'
    filter_backends = [DynamicSearchFilter, django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]

    def get_queryset(self):
        id_only = self.request.query_params.get('id_only', None)
        if id_only:
            self.serializer_class = OrderIdsSerializer
        return self.queryset


class SingleOrder(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AdminCustomPermission,)


class Families(ListCreateAPIView):
    queryset = Family.objects.all()
    write_serializer_class = FamilySerializer
    read_serializer_class = FamilyReadSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission,)
    search_fields = ['scientific_names__name']
    filterset_fields = ['scientific_names__name']
    ordering_fields = '__all__'
    filter_backends = [DynamicSearchFilter, django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]

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
    permission_classes = (AdminCustomPermission,)


class Authors(ListCreateAPIView):
    queryset = MultimediaAuthor.objects.all()
    read_serializer_class = AuthorMediaSerializer
    write_serializer_class = AuthorSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminCustomPermission,)
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['first_name', 'last_name', 'email']
    ordering_fields = '__all__'
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        queryset = self.queryset
        media_type = self.request.query_params.get('media_type', None)
        if media_type == 'images':
            queryset = self.queryset.filter(images_authored__isnull=False).distinct()
        elif media_type == 'videos':
            queryset = self.queryset.filter(videos_authored__isnull=False).distinct()
        elif media_type == 'audios':
            queryset = self.queryset.filter(audios_authored__isnull=False).distinct()
        id_only = self.request.query_params.get('id_only', None)
        if id_only:
            self.read_serializer_class = AuthorIdsSerializer
        return queryset


class SingleAuthor(RetrieveUpdateDestroyAPIView):
    queryset = MultimediaAuthor.objects.all()
    read_serializer_class = AuthorMediaSerializer
    write_serializer_class = AuthorSerializer
    permission_classes = (AdminCustomPermission,)


@api_view(['GET'])
def get_names(request):
    model = request.query_params.get('model', None)
    if model:
        if model == 'feeding':
            names = list(Bird.objects.order_by().values_list('feeding__names__text', flat=True).distinct())
        else:
            try:
                names = list(Bird.objects.order_by().values_list(model + '__name__text', flat=True).distinct())
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


@api_view(['POST'])
@permission_classes((AdminCustomPermission, ))
def exists_bird_file(request):
    path = handle_uploaded_file(request.FILES['file'])
    response = bird_exists(os.path.join(settings.MEDIA_ROOT, path))
    delete_uploaded_file(path)
    if response['success']:
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((AdminCustomPermission, ))
def upload_bird_file(request):
    path = handle_uploaded_file(request.FILES['file'])
    response = doc_to_model(os.path.join(settings.MEDIA_ROOT, path))
    delete_uploaded_file(path)
    if response['success']:
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
