from django.contrib import admin

from birds.models import Text, Reference, Author, Order, Family, Identification, Reproduction, \
    Bird, Image, Video, Audio, Value, Type, Subspecies, SubspeciesName, BirdImage, Measure


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('language', 'text',)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('referenced', 'type', 'title', 'year', 'series', 'volume', 'edition', 'isbn', 'publisher', 'doi',
                    'url', 'initial_page', 'last_page', 'date_accessed',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'reference', 'image', 'url', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ('inferior', 'superior', 'average')


@admin.register(Identification)
class IdentificationAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(Type)
class HabitatAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'text')


@admin.register(Reproduction)
class ReproductionAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = ('id', 'family', 'description', 'identification', 'habitat',
                    'reproduction', 'taxonomy', 'conservation',
                    'own_citation', 'last_updated',)


@admin.register(Subspecies)
class SubspeciesAdmin(admin.ModelAdmin):
    list_display = ('distribution',)


@admin.register(SubspeciesName)
class SubspeciesNameAdmin(admin.ModelAdmin):
    list_display = ('name','main')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'format', 'height', 'width', 'url')


@admin.register(BirdImage)
class BirdImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'thumbnail', 'category', 'format', 'location', 'height', 'width', 'bird')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('url', 'thumbnail', 'category', 'format', 'location', 'seconds', 'bird')


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('url', 'author', 'format', 'location', 'bird')


@admin.register(Measure)
class LengthAdmin(admin.ModelAdmin):
    list_display = ('value', 'unit', 'identification_lengths', 'identification_weights')
