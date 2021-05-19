from django.contrib.auth.models import AbstractUser
# from django.db import models
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
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


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
    image = models.ForeignKey('Image', related_name='type_image', null=True, on_delete=models.SET_NULL)
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='type_text')
    identification = models.ForeignKey(Identification, null=True, on_delete=models.SET_NULL, related_name='plumage')
    bird_feeding = models.ForeignKey('Bird', null=True, on_delete=models.SET_NULL, related_name='feeding')
    reproduction = models.ForeignKey('Bird', null=True, on_delete=models.SET_NULL, related_name='reproduction')
    bird_behavior = models.ForeignKey('Bird', null=True, on_delete=models.SET_NULL, related_name='behavior')


class Image(models.Model):
    url = models.URLField(unique=True)
    thumbnail = models.URLField(null=True, blank=True)
    format = models.CharField(max_length=4, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)


class Distribution(models.Model):
    text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='distribution')
    location_map = models.ForeignKey(Image, null=True, on_delete=models.SET_NULL, related_name='distribution')

#
# class SDYouth(models.Model):
#     image = models.ForeignKey('BirdImage', related_name='sdyouth', null=True, on_delete=models.SET_NULL)
#     text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='sdyouth')
#
#
# class SDSubadult(models.Model):
#     image = models.ForeignKey('BirdImage', related_name='sdsubadult', null=True, on_delete=models.SET_NULL)
#     text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='sdsubadult')
#
#
# class SDFemale(models.Model):
#     image = models.ForeignKey('BirdImage', related_name='sdfemale', null=True, on_delete=models.SET_NULL)
#     text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='sdfemale')
#
#
# class SDMale(models.Model):
#     image = models.ForeignKey('BirdImage', related_name='sdmale', null=True, on_delete=models.SET_NULL)
#     text = models.ForeignKey(Text, null=True, on_delete=models.SET_NULL, related_name='sdmale')
#
#
# class SexualDifferentiation(models.Model):
#     youth = models.ForeignKey(SDYouth, null=True, on_delete=models.SET_NULL, related_name='sexual_diff')
#     subadult = models.ForeignKey(SDSubadult, null=True, on_delete=models.SET_NULL, related_name='sexual_diff')
#     female = models.ForeignKey(SDFemale, null=True, on_delete=models.SET_NULL, related_name='sexual_diff')
#     male = models.ForeignKey(SDMale, null=True, on_delete=models.SET_NULL, related_name='sexual_diff')


class Bird(models.Model):
    # common_names = models.ManyToManyField(Text, through='CommonNameBird', related_name='birds_cn')
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
    similar_species_class_id = models.ForeignKey('SimilarSpecies', related_name='bird_ids', null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(Author, through='AuthorBird', related_name='bird_authors')
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
    BIRD = 'BIRD'
    FAMILY = 'FAMILY'
    ORDER = 'ORDER'
    SUBSPECIES = 'SUBSPECIES'
    CATEGORY_CHOICES = (
        ('BIRD', BIRD),
        ('FAMILY', FAMILY),
        ('ORDER', ORDER),
        ('SUBSPECIES', SUBSPECIES),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    main = models.BooleanField(default=False)
    bird = models.ForeignKey(Bird, related_name='images', null=True, on_delete=models.SET_NULL)
    subspecies = models.ForeignKey(Subspecies, related_name='images', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Author, related_name='images_authored', null=True, on_delete=models.SET_NULL)


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
    author = models.ForeignKey(Author, related_name='videos_authored', null=True, on_delete=models.SET_NULL)


class Audio(models.Model):
    url = models.URLField(unique=True)
    author = models.ForeignKey(Author, related_name='audios_authored', null=True, on_delete=models.SET_NULL)
    format = models.CharField(max_length=4)
    location = models.PointField(null=True, blank=True)


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
    audio = models.ForeignKey(Audio, related_name='vocalization', null=True, on_delete=models.SET_NULL)
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
    name = models.CharField(max_length=100) # in spanish
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES)
    reference = models.ForeignKey(Reference, related_name='measures', null=True, on_delete=models.SET_NULL)
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
