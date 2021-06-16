from django.contrib import admin

from birds.models import Text, Reference, Author, Order, Family, Identification, \
    Bird, Image, Video, Audio, Value, Type, Subspecies, SubspeciesName, BirdImage, Measure, CommonNameBird, \
    Vocalization, Distribution, Feeding


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('language', 'text',)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('referenced', 'type', 'title', 'year', 'series', 'volume', 'edition', 'isbn', 'publisher', 'doi',
                    'url', 'initial_page', 'last_page', 'date_accessed',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'reference', 'image', 'webpage', 'description')


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
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')


@admin.register(Feeding)
class FeedingAdmin(admin.ModelAdmin):
    list_display = ('id','text')


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('text', 'location_map')


class CNInlineAdmin(admin.TabularInline):
    model = CommonNameBird


@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = ('id', 'family', 'description', 'identification',
                    'habitat', 'taxonomy', 'conservation',
                    'own_citation', 'last_updated',)
    inlines = [CNInlineAdmin]


@admin.register(Subspecies)
class SubspeciesAdmin(admin.ModelAdmin):
    list_display = ('distribution',)


@admin.register(SubspeciesName)
class SubspeciesNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'main')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'format', 'height', 'width', 'url')


@admin.register(BirdImage)
class BirdImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'thumbnail', 'category', 'format', 'location', 'height', 'width', 'bird', 'main')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('url', 'thumbnail', 'category', 'format', 'location', 'duration_in_seconds', 'bird')


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('url', 'author', 'format', 'location')


@admin.register(Vocalization)
class VocalizationAdmin(admin.ModelAdmin):
    list_display = ('bird', 'audio', 'category', 'short_description', 'long_description')


@admin.register(Measure)
class LengthAdmin(admin.ModelAdmin):
    list_display = ('value', 'unit', 'identification_lengths', 'identification_weights')
