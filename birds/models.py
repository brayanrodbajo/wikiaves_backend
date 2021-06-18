from django.contrib.auth.models import AbstractUser
# from django.db import models
from django.contrib.gis.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class Text(models.Model):
    ES = 'es'
    EN = 'en'
    LANGUAGE_CHOICES = (
        ('es', ES),
        ('en', EN),
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    text = models.TextField()
    feeding_name = models.ForeignKey('Feeding', null=True, on_delete=models.SET_NULL, related_name='names')


class Reference(models.Model):
    LITERATURE = 'LITERATURE'
    MAP = 'MAP'
    IMAGE = 'IMAGE'
    AUDIO = 'AUDIO'
    VIDEO = 'VIDEO'
    BIRD = 'BIRD'
    MEASURE = 'MEASURE'
    REFERENCED_CHOICES = (
        ('LITERATURE', LITERATURE),
        ('MAPS', MAP),
        ('IMAGES', IMAGE),
        ('AUDIO', AUDIO),
        ('VIDEO', VIDEO),
        ('BIRD', BIRD),
        ('MEASURE', MEASURE),
    )
    referenced = models.CharField(max_length=10, choices=REFERENCED_CHOICES)
    type = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    series = models.IntegerField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    edition = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    publisher = models.CharField(max_length=50, null=True, blank=True)
    doi = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    initial_page = models.IntegerField(null=True, blank=True)
    last_page = models.IntegerField(null=True, blank=True)
    date_accessed = models.DateTimeField(null=True, blank=True)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    reference = models.ForeignKey(Reference, related_name='authors', null=True, on_delete=models.SET_NULL)
    image = models.ForeignKey('Image', related_name='author_image', null=True, on_delete=models.SET_NULL)
    webpage = models.URLField(null=True, blank=True)
    description = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='author_description')
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    flicker = models.URLField(null=True, blank=True)


class Order(models.Model):
    pass  # the field is scientific_names in the ScientificNameOrder model


class Family(models.Model):
    order = models.ForeignKey(Order, related_name='family', null=True, on_delete=models.SET_NULL)


class Value(models.Model):
    inferior = models.FloatField(null=True, blank=True)
    superior = models.FloatField(null=True, blank=True)
    average = models.FloatField(null=True, blank=True)


class Identification(models.Model):
    description = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL,
                                    related_name='identification_description')


class Type(models.Model):
    name = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='type_name')
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='type_text')
    reproduction = models.ForeignKey('Bird', null=True, on_delete=models.SET_NULL, related_name='reproduction')
    bird_behavior = models.ForeignKey('Bird', null=True, on_delete=models.SET_NULL, related_name='behavior')


def upload_images(instance, filename):
    return 'images/{filename}'.format(filename=filename)


def upload_images_tn(instance, filename):
    return 'images/thumbnails/{filename}'.format(filename=filename)


class Image(models.Model):
    url = models.ImageField(upload_to=upload_images, max_length=500)
    thumbnail = models.ImageField(null=True, blank=True, upload_to=upload_images_tn, max_length=500)
    format = models.CharField(max_length=4, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)


class Distribution(models.Model):
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='distribution')
    location_map = models.ForeignKey(Image, null=True, on_delete=models.SET_NULL, related_name='distribution')


class Feeding(models.Model):
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='feeding')


class Bird(models.Model):
    family = models.ForeignKey(Family, related_name='bird', null=True, on_delete=models.SET_NULL)
    description = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='birds_desc')
    identification = models.ForeignKey(Identification, related_name='bird', null=True, on_delete=models.SET_NULL)
    distribution = models.ForeignKey(Distribution, null=True, on_delete=models.SET_NULL, related_name='birds_dist')
    habitat = models.ForeignKey(Text, related_name='bird', null=True, on_delete=models.SET_NULL)
    taxonomy = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='birds_tax')
    conservation = models.ForeignKey(Type, related_name='bird_conservation', null=True, on_delete=models.SET_NULL)
    references = models.ManyToManyField(Reference, through='ReferencesBird', related_name='bird_refs')
    migration = models.ForeignKey(Type, related_name='bird_migration', null=True, on_delete=models.SET_NULL)
    own_citation = models.ForeignKey(Reference, related_name='bird', null=True, on_delete=models.SET_NULL)
    similar_species = models.ForeignKey('SimilarSpecies', related_name='bird', null=True, on_delete=models.SET_NULL)
    similar_species_class_id = models.ForeignKey('SimilarSpecies', related_name='bird_ids', null=True,
                                                 on_delete=models.SET_NULL)
    feeding = models.ForeignKey(Feeding, null=True, on_delete=models.SET_NULL, related_name='birds_feed')
    authors = models.ManyToManyField(Author, through='AuthorBird', related_name='bird_authors')
    draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class AuthorBird(models.Model):
    author = models.ForeignKey(Author, related_name='authors_bird', null=True, on_delete=models.SET_NULL)
    bird = models.ForeignKey(Bird, related_name='authors_bird', null=True, on_delete=models.SET_NULL)


class SimilarSpecies(models.Model):
    text = models.ForeignKey(Text, related_name='similar_species', null=True, on_delete=models.SET_NULL)


class ReferencesBird(models.Model):
    reference = models.ForeignKey(Reference, related_name='references_bird', null=True, on_delete=models.SET_NULL)
    bird = models.ForeignKey(Bird, related_name='references_bird', null=True, on_delete=models.SET_NULL)


class Subspecies(models.Model):
    distribution = models.ForeignKey(Distribution, null=True, on_delete=models.SET_NULL, related_name='subspecies_dist')
    bird = models.ForeignKey(Bird, related_name='subspecies', null=True, on_delete=models.SET_NULL)


class SubspeciesName(models.Model):
    subspecies = models.ForeignKey(Subspecies, related_name='names', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    main = models.BooleanField(default=False)


class BirdImage(Image):
    category = models.CharField(max_length=50, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    main = models.BooleanField(default=False)
    bird = models.ForeignKey(Bird, related_name='images', null=True, on_delete=models.SET_NULL)
    subspecies = models.ForeignKey(Subspecies, related_name='images', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Author, related_name='images_authored', null=True, on_delete=models.SET_NULL)


def upload_videos(instance, filename):
    return 'videos/{filename}'.format(filename=filename)


def upload_videos_tn(instance, filename):
    return 'videos/thumbnails/{filename}'.format(filename=filename)


class Video(models.Model):
    url = models.FileField(upload_to=upload_videos, max_length=500)
    thumbnail = models.ImageField(null=True, blank=True, upload_to=upload_videos_tn, max_length=500)
    category = models.CharField(max_length=50, null=True, blank=True)
    format = models.CharField(max_length=4, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    duration_in_seconds = models.FloatField(null=True, blank=True)
    bird = models.ForeignKey(Bird, related_name='videos', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Author, related_name='videos_authored', null=True, on_delete=models.SET_NULL)


def upload_audios(instance, filename):
    return 'audios/{filename}'.format(filename=filename)


class Audio(models.Model):
    url = models.FileField(upload_to=upload_audios, max_length=500)
    author = models.ForeignKey(Author, related_name='audios_authored', null=True, on_delete=models.SET_NULL)
    format = models.CharField(max_length=4, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    vocalization = models.ForeignKey('Vocalization', related_name='audios', null=True, on_delete=models.SET_NULL)


class Xenocanto(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    url = models.URLField()
    vocalization = models.ForeignKey('Vocalization', related_name='xenocantos', null=True, on_delete=models.SET_NULL)


class Vocalization(models.Model):
    SONG = 'SONG'
    CALL = 'CALL'
    CATEGORY_CHOICES = (
        ('SONG', SONG),
        ('CALL', CALL)
    )
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES)
    short_description = models.ForeignKey(Text, related_name='vocalization_short', null=True, on_delete=models.SET_NULL)
    long_description = models.ForeignKey(Text, related_name='vocalization_long', null=True, on_delete=models.SET_NULL)
    bird = models.ForeignKey(Bird, related_name='vocalizations', null=True, on_delete=models.SET_NULL)


class Measure(models.Model):
    CM = 'cm'
    MM = 'mm'
    IN = 'in'
    GR = 'g'
    KG = 'kg'
    UNIT_CHOICES = (
        ('cm', CM),
        ('mm', MM),
        ('in', IN),
        ('g', GR),
        ('kg', KG),
    )
    value = models.ForeignKey(Value, null=True, related_name='measure', on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)  # in spanish
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES)
    reference = models.TextField(null=True, blank=True)
    identification_lengths = models.ForeignKey(Identification, related_name='lengths', null=True,
                                               on_delete=models.SET_NULL)
    identification_weights = models.ForeignKey(Identification, related_name='weights', null=True,
                                               on_delete=models.SET_NULL)
    identification_lengths_subs = models.ForeignKey(Subspecies, related_name='lengths', null=True,
                                                    on_delete=models.SET_NULL)
    identification_weights_subs = models.ForeignKey(Subspecies, related_name='weights', null=True,
                                                    on_delete=models.SET_NULL)


class ScientificNameOrder(models.Model):
    order = models.ForeignKey(Order, related_name='scientific_names', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    main = models.BooleanField(default=False)


class ScientificNameFamily(models.Model):
    family = models.ForeignKey(Family, related_name='scientific_names', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    main = models.BooleanField(default=False)


class CommonNameBird(models.Model):
    bird = models.ForeignKey(Bird, related_name='common_names', null=True, on_delete=models.SET_NULL)
    name = models.ForeignKey(Text, related_name='common_name_bird', null=True, on_delete=models.SET_NULL)
    main = models.BooleanField(default=False)


class ScientificNameBird(models.Model):
    bird = models.ForeignKey(Bird, related_name='scientific_names', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    main = models.BooleanField(default=False)
