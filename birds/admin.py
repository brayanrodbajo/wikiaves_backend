from django.contrib import admin

from birds.models import Text, Reference, Author, Order, Family, Identification, Habitat, Feeding, Reproduction, \
    Conservation, Bird, Image, Video, Audio, Length


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('language', 'text',)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('referenced', 'type', 'title', 'year', 'series', 'volume', 'edition', 'isbn', 'publisher', 'doi', 'url', 'initial_page', 'last_page', 'date_accessed',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'reference')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('scientific_name', 'common_names',)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('scientific_name','common_names','order')


@admin.register(Identification)
class IdentificationAdmin(admin.ModelAdmin):
    list_display = ('size_shape', 'similar_species', 'regional_differences')


@admin.register(Habitat)
class HabitatAdmin(admin.ModelAdmin):
    list_display = ('type', 'text')


@admin.register(Feeding)
class FeedingAdmin(admin.ModelAdmin):
    list_display = ('type', 'text')


@admin.register(Reproduction)
class ReproductionAdmin(admin.ModelAdmin):
    list_display = ('type', 'text')


@admin.register(Conservation)
class ConservationAdmin(admin.ModelAdmin):
    list_display = ('type', 'text')


@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = ('scientific_name','common_names','family','description','identification','distribution','habitat','feeding','reproduction','behavior','taxonomy','conservation','curiosities','references','own_citation','last_updated',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'thumbnail', 'category', 'format', 'location', 'height', 'width', 'bird')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('url', 'thumbnail', 'category', 'format', 'location', 'seconds', 'bird')


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('url', 'author', 'format', 'location', 'bird')


@admin.register(Length)
class LengthAdmin(admin.ModelAdmin):
    list_display = ('length', 'unit', 'bird')


