from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models


class Text(models.Model):
    ES = 'es'
    EN = 'en'
    LANGUAGE_CHOICES = (
        ('es', ES),
        ('en', EN),
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    text = models.TextField()


class Reference(models.Model):
    LITERATURE = 'LITERATURE'
    MAP = 'MAP'
    IMAGE = 'IMAGE'
    AUDIO = 'AUDIO'
    VIDEO = 'VIDEO'
    BIRD = 'BIRD'
    REFERENCED_CHOICES = (
        ('LITERATURE', LITERATURE),
        ('MAPS', MAP),
        ('IMAGES', IMAGE),
        ('AUDIO', AUDIO),
        ('VIDEO', VIDEO),
        ('BIRD', BIRD),
    )
    referenced = models.CharField(max_length=10, choices=REFERENCED_CHOICES)
    type = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    series = models.IntegerField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    edition = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    publisher = models.CharField(max_length=13, null=True, blank=True)
    doi = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    initial_page = models.IntegerField(null=True, blank=True)
    last_page = models.IntegerField(null=True, blank=True)
    date_accessed = models.DateTimeField(null=True, blank=True)


class Author(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    reference = models.ForeignKey(Reference, related_name='authors', on_delete=models.PROTECT)


class Order(models.Model):
    scientific_name = models.CharField(max_length=500, unique=True)
    common_names = models.ManyToManyField(Text, through='CommonNameOrder', null=True)


class Family(models.Model):
    scientific_name = models.CharField(max_length=500, unique=True)
    common_names = models.ManyToManyField(Text, through='CommonNameFamily', null=True)
    order = models.ForeignKey(Order, related_name='family', on_delete=models.PROTECT, null=True)


class Identification(models.Model):
    size_shape = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)
    similar_species = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)
    regional_differences = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)


class Habitat(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)


class Feeding(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)


class Reproduction(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)


class Conservation(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)


class Bird(models.Model):
    scientific_name = models.CharField(max_length=500, unique=True)
    common_names = models.ManyToManyField(Text, through='CommonNameBird', null=True)
    family = models.ForeignKey(Family, related_name='bird', on_delete=models.PROTECT, null=True)
    description = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)
    identification = models.ForeignKey(Identification, related_name='bird', on_delete=models.PROTECT, null=True)
    distribution = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)
    habitat = models.ForeignKey(Habitat, related_name='bird', on_delete=models.PROTECT, null=True)
    feeding = models.ForeignKey(Feeding, related_name='bird', on_delete=models.PROTECT, null=True)
    reproduction = models.ForeignKey(Reproduction, related_name='bird', on_delete=models.PROTECT, null=True)
    behavior = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)
    taxonomy = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)
    conservation = models.ForeignKey(Conservation, related_name='bird', on_delete=models.PROTECT, null=True)
    curiosities = models.ForeignKey(Text, on_delete=models.PROTECT, null=True)
    references = models.ManyToManyField(Reference, through='ReferencesBird', related_name='bird_refs')
    own_citation = models.ForeignKey(Reference, related_name='bird', on_delete=models.PROTECT)
    last_updated = models.DateTimeField(auto_now=True)


class ReferencesBird(models.Model):
    reference = models.ForeignKey(Reference, related_name='references_bird', on_delete=models.PROTECT)
    bird = models.ForeignKey(Bird, related_name='references_bird', on_delete=models.PROTECT)


class Image(models.Model):
    BIRD = 'BIRD'
    FAMILY = 'FAMILY'
    ORDER = 'ORDER'
    CATEGORY_CHOICES = (
        ('BIRD', BIRD),
        ('FAMILY', FAMILY),
        ('ORDER', ORDER),
    )
    url = models.URLField(unique=True)
    thumbnail = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES, null=True, blank=True)
    format = models.CharField(max_length=4)
    location = models.PointField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    bird = models.ForeignKey(Bird, related_name='images', on_delete=models.PROTECT)


class Video(models.Model):
    BIRD = 'BIRD'
    FAMILY = 'FAMILY'
    ORDER = 'ORDER'
    CATEGORY_CHOICES = (
        ('BIRD', BIRD),
        ('FAMILY', FAMILY),
        ('ORDER', ORDER),
    )
    url = models.URLField(unique=True)
    thumbnail = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES, null=True, blank=True)
    format = models.CharField(max_length=4)
    location = models.PointField(null=True, blank=True)
    seconds = models.FloatField(null=True, blank=True)
    bird = models.ForeignKey(Bird, related_name='videos', on_delete=models.PROTECT)


class Audio(models.Model):
    BIRD = 'BIRD'
    FAMILY = 'FAMILY'
    ORDER = 'ORDER'
    CATEGORY_CHOICES = (
        ('BIRD', BIRD),
        ('FAMILY', FAMILY),
        ('ORDER', ORDER),
    )
    url = models.URLField(unique=True)
    author = models.ForeignKey(Author, related_name='audio', on_delete=models.PROTECT)
    format = models.CharField(max_length=4)
    location = models.PointField(null=True, blank=True)
    bird = models.ForeignKey(Bird, related_name='singing', on_delete=models.PROTECT)


class Length(models.Model):
    CM = 'cm'
    IN = 'in'
    UNIT_CHOICES = (
        ('cm', CM),
        ('in', IN),
    )
    length = models.FloatField()
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES)
    bird = models.ForeignKey(Bird, related_name='height', on_delete=models.PROTECT)


class CommonNameOrder(models.Model):
    order = models.ForeignKey(Order, related_name='common_name_order', on_delete=models.PROTECT)
    text = models.ForeignKey(Text, related_name='common_name_order', on_delete=models.PROTECT)


class CommonNameFamily(models.Model):
    family = models.ForeignKey(Family, related_name='common_name_family', on_delete=models.PROTECT)
    text = models.ForeignKey(Text, related_name='common_name_family', on_delete=models.PROTECT)


class CommonNameBird(models.Model):
    bird = models.ForeignKey(Bird, related_name='common_name_bird', on_delete=models.PROTECT)
    text = models.ForeignKey(Text, related_name='common_name_bird', on_delete=models.PROTECT)




