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
    reference = models.ForeignKey(Reference, related_name='authors', null=True, on_delete=models.SET_NULL)


class Order(models.Model):
    scientific_name = models.CharField(max_length=500, unique=True)
    common_names = models.ManyToManyField(Text, through='CommonNameOrder')


class Family(models.Model):
    scientific_name = models.CharField(max_length=500, unique=True)
    common_names = models.ManyToManyField(Text, through='CommonNameFamily')
    order = models.ForeignKey(Order, related_name='family', null=True, on_delete=models.SET_NULL)


class Identification(models.Model):
    size_shape = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='identification_shape')
    similar_species = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='identification_species')
    regional_differences = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='identification_rd')


class Habitat(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='habitat')


class Feeding(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='feeding')


class Reproduction(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='reproduction')


class Conservation(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='conservation')


class Bird(models.Model):
    scientific_name = models.CharField(max_length=500, unique=True)  # TODO: Check if there could be multiple
    common_names = models.ManyToManyField(Text, through='CommonNameBird', related_name='birds_cn')
    family = models.ForeignKey(Family, related_name='bird', null=True, on_delete=models.SET_NULL)
    description = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='birds_desc')
    identification = models.ForeignKey(Identification, related_name='bird', null=True, on_delete=models.SET_NULL)
    distribution = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='birds_dist')
    habitat = models.ForeignKey(Habitat, related_name='bird', null=True, on_delete=models.SET_NULL)
    feeding = models.ForeignKey(Feeding, related_name='bird', null=True, on_delete=models.SET_NULL)
    reproduction = models.ForeignKey(Reproduction, related_name='bird', null=True, on_delete=models.SET_NULL)
    behavior = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='birds_beh')
    taxonomy = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='birds_tax')
    conservation = models.ForeignKey(Conservation, related_name='bird', null=True, on_delete=models.SET_NULL)
    curiosities = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='birds_cur')
    references = models.ManyToManyField(Reference, through='ReferencesBird', related_name='bird_refs')
    own_citation = models.ForeignKey(Reference, related_name='bird', null=True, on_delete=models.SET_NULL)
    last_updated = models.DateTimeField(auto_now=True)


class ReferencesBird(models.Model):
    reference = models.ForeignKey(Reference, related_name='references_bird', null=True, on_delete=models.SET_NULL)
    bird = models.ForeignKey(Bird, related_name='references_bird', null=True, on_delete=models.SET_NULL)


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
    bird = models.ForeignKey(Bird, related_name='images', null=True, on_delete=models.SET_NULL)


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
    bird = models.ForeignKey(Bird, related_name='videos', null=True, on_delete=models.SET_NULL)


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
    author = models.ForeignKey(Author, related_name='audio', null=True, on_delete=models.SET_NULL)
    format = models.CharField(max_length=4)
    location = models.PointField(null=True, blank=True)
    bird = models.ForeignKey(Bird, related_name='singing', null=True, on_delete=models.SET_NULL)


class Length(models.Model):
    CM = 'cm'
    IN = 'in'
    UNIT_CHOICES = (
        ('cm', CM),
        ('in', IN),
    )
    length = models.FloatField()
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES)
    bird = models.ForeignKey(Bird, related_name='heights', null=True, on_delete=models.SET_NULL)


class CommonNameOrder(models.Model):
    order = models.ForeignKey(Order, related_name='common_name_order', null=True, on_delete=models.SET_NULL)
    text = models.ForeignKey(Text, related_name='common_name_order', null=True, on_delete=models.SET_NULL)


class CommonNameFamily(models.Model):
    family = models.ForeignKey(Family, related_name='common_name_family', null=True, on_delete=models.SET_NULL)
    text = models.ForeignKey(Text, related_name='common_name_family', null=True, on_delete=models.SET_NULL)


class CommonNameBird(models.Model):
    bird = models.ForeignKey(Bird, related_name='common_name_bird', null=True, on_delete=models.SET_NULL)
    text = models.ForeignKey(Text, related_name='common_name_bird', null=True, on_delete=models.SET_NULL)




