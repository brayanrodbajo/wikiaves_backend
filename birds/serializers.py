from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from birds.models import Text, Author, Image, ScientificNameOrder, ScientificNameFamily, CommonNameBird, \
    ScientificNameBird, Order, Family, Identification, Type, Measure, Value, Reproduction, Reference, Bird, Video, \
    BirdImage, Audio, Subspecies, SubspeciesName, Vocalization, Distribution, SimilarSpecies


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ('id',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ('id',)
        extra_kwargs = {
            'url': {'validators': []},
        }


class AuthorSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False)

    class Meta:
        model = Author
        exclude = ('id', 'reference')

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        if image:
            serializer = ImageSerializer(data=image)
            if serializer.is_valid():
                image = serializer.save()
            else:
                print(serializer.errors)
        author = Author.objects.create(image=image, **validated_data)
        return author

    def update(self, instance, validated_data):
        image = validated_data.get('image', None)
        if image:
            serializer = ImageSerializer(instance.image, data=image)
            if serializer.is_valid():
                image = serializer.save()
                instance.image = image
            else:
                print(serializer.errors)
        instance.first_name = validated_data.get('first_name', None)
        instance.last_name = validated_data.get('last_name', None)
        instance.url = validated_data.get('url', None)
        instance.description = validated_data.get('description', None)
        instance.save()
        return instance


class ScientificNameOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScientificNameOrder
        fields = ('name', 'main')


class ScientificNameFamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = ScientificNameFamily
        fields = ('name', 'main')


class CommonNameBirdSerializer(serializers.ModelSerializer):
    name = TextSerializer(required=False)

    class Meta:
        model = CommonNameBird
        fields = ('name', 'main')

    def create(self, validated_data):
        name = validated_data.pop('name', None)
        if name:
            serializer = TextSerializer(data=name)
            if serializer.is_valid():
                name = serializer.save()
            else:
                print(serializer.errors)
        c_n = CommonNameBird.objects.create(name=name, **validated_data)
        return c_n

    def update(self, instance, validated_data):
        name = validated_data.get('name', None)
        if name:
            serializer = TextSerializer(instance.name, data=name)
            if serializer.is_valid():
                name = serializer.save()
                instance.name = name
            else:
                print(serializer.errors)
        instance.main = validated_data.get('main', None)
        instance.save()
        return instance


class SimilarSpeciesSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)
    bird_ids = PrimaryKeyRelatedField(many=True, queryset=Bird.objects.all(), required=False)

    class Meta:
        model = SimilarSpecies
        fields = ('text', 'bird_ids')

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        similar_species_data = validated_data.pop('bird_ids', [])
        bird_ids = []
        for ss in similar_species_data:
            if isinstance(ss, Bird):
                bird_ids.append(ss)
        obj = SimilarSpecies.objects.create(text=text)
        obj.bird_ids.set(bird_ids)
        return obj

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        similar_species_data = validated_data.pop('bird_ids', [])
        bird_ids = []
        for ss in similar_species_data:
            if isinstance(ss, Bird):
                bird_ids.append(ss)
        instance.bird_ids.set(bird_ids)
        instance.save()
        return instance


class ScientificNameBirdSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScientificNameBird
        fields = ('name', 'main')


class OrderSerializer(serializers.ModelSerializer):
    scientific_names = ScientificNameOrderSerializer(required=False, many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        scientific_names_data = validated_data.pop('scientific_names', [])
        order = Order.objects.create(**validated_data)
        scientific_names = []
        for scientific_name in scientific_names_data:
            serializer = ScientificNameOrderSerializer(data=scientific_name)
            if serializer.is_valid():
                c_n = serializer.save()
                scientific_names.append(c_n)
            else:
                print(serializer.errors)
        order.scientific_names.set(scientific_names)
        return order

    def update(self, instance, validated_data):
        scientific_names_data = validated_data.get('scientific_names', [])
        scientific_names = []
        instance.scientific_names.all().delete()
        for scientific_name in scientific_names_data:
            serializer = ScientificNameOrderSerializer(data=scientific_name)
            if serializer.is_valid():
                c_n = serializer.save()
                scientific_names.append(c_n)
            else:
                print(serializer.errors)
        instance.scientific_names.set(scientific_names)
        instance.save()
        return instance


class FamilySerializer(serializers.ModelSerializer):
    scientific_names = ScientificNameFamilySerializer(required=False, many=True)
    order = PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)

    class Meta:
        model = Family
        fields = '__all__'

    def create(self, validated_data):
        order = validated_data.pop('order', None)
        scientific_names_data = validated_data.pop('scientific_names', [])
        family = Family.objects.create(order=order, **validated_data)
        scientific_names = []
        for scientific_name in scientific_names_data:
            serializer = ScientificNameFamilySerializer(data=scientific_name)
            if serializer.is_valid():
                c_n = serializer.save()
                scientific_names.append(c_n)
            else:
                print(serializer.errors)
        family.scientific_names.set(scientific_names)
        return family

    def update(self, instance, validated_data):
        order = validated_data.get('order', None)
        if order:
            instance.order = order
        scientific_names_data = validated_data.get('scientific_names', [])
        scientific_names = []
        instance.scientific_names.all().delete()
        for scientific_name in scientific_names_data:
            serializer = ScientificNameFamilySerializer(data=scientific_name)
            if serializer.is_valid():
                c_n = serializer.save()
                scientific_names.append(c_n)
            else:
                print(serializer.errors)
        instance.scientific_names.set(scientific_names)
        instance.save()
        return instance


class TypeSerializer(serializers.ModelSerializer):
    name = TextSerializer(required=False)
    image = ImageSerializer(required=False)
    text = TextSerializer(required=False)

    class Meta:
        model = Type
        exclude = ('id', 'identification', 'bird_feeding', 'reproduction', 'bird_behavior')

    def create(self, validated_data):
        name = validated_data.pop('name', None)
        image = validated_data.pop('image', None)
        text = validated_data.pop('text', None)
        if name:
            serializer = TextSerializer(data=name)
            if serializer.is_valid():
                name = serializer.save()
            else:
                print(serializer.errors)
        if image:
            serializer = ImageSerializer(data=image)
            if serializer.is_valid():
                image = serializer.save()
            else:
                print(serializer.errors)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        type = Type.objects.create(name=name, image=image, text=text)
        return type

    def update(self, instance, validated_data):
        name = validated_data.get('name', None)
        if name:
            serializer = TextSerializer(instance.name, data=name)
            if serializer.is_valid():
                name = serializer.save()
                instance.name = name
            else:
                print(serializer.errors)
        image = validated_data.get('image', None)
        if image:
            serializer = ImageSerializer(instance.image, data=image)
            if serializer.is_valid():
                image = serializer.save()
                instance.text = image
            else:
                print(serializer.errors)
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        instance.save()
        return instance


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        exclude = ('id',)


class MeasureSerializer(serializers.ModelSerializer):
    value = ValueSerializer(required=False)

    class Meta:
        model = Measure
        fields = ('value', 'unit', 'name')

    def create(self, validated_data):
        value = validated_data.pop('value', None)
        if value:
            serializer = ValueSerializer(data=value)
            if serializer.is_valid():
                value = serializer.save()
            else:
                print(serializer.errors)
        measure = Measure.objects.create(value=value, **validated_data)
        return measure

    def update(self, instance, validated_data):
        value = validated_data.get('value', None)
        if value:
            serializer = ValueSerializer(instance.value, data=value)
            if serializer.is_valid():
                value = serializer.save()
                instance.value = value
            else:
                print(serializer.errors)
        instance.name = validated_data.get('name', None)
        instance.unit = validated_data.get('unit', None)
        instance.save()
        return instance


class IdentificationSerializer(serializers.ModelSerializer):
    description = TextSerializer(required=False)
    plumage = TypeSerializer(required=False, many=True)
    lengths = MeasureSerializer(required=False, many=True)
    weights = MeasureSerializer(required=False, many=True)

    class Meta:
        model = Identification
        exclude = ('id',)

    def create(self, validated_data):
        description = validated_data.pop('description', None)
        plumage_data = validated_data.pop('plumage', [])
        lengths_data = validated_data.pop('lengths', [])
        weights_data = validated_data.pop('weights', [])
        if description:
            serializer = TextSerializer(data=description)
            if serializer.is_valid():
                description = serializer.save()
            else:
                print(serializer.errors)
        identification = Identification.objects.create(description=description, **validated_data)
        plumage = []
        for plum in plumage_data:
            serializer = TypeSerializer(data=plum)
            if serializer.is_valid():
                obj = serializer.save()
                plumage.append(obj)
            else:
                print(serializer.errors)
        identification.plumage.set(plumage)
        lengths = []
        for len in lengths_data:
            serializer = MeasureSerializer(data=len)
            if serializer.is_valid():
                obj = serializer.save()
                lengths.append(obj)
            else:
                print(serializer.errors)
        identification.lengths.set(lengths)
        weights = []
        for wei in weights_data:
            serializer = MeasureSerializer(data=wei)
            if serializer.is_valid():
                obj = serializer.save()
                weights.append(obj)
            else:
                print(serializer.errors)
        identification.weights.set(weights)
        return identification

    def update(self, instance, validated_data):
        plumage_data = validated_data.pop('plumage', [])
        plumage = []
        instance.plumage.all().delete()
        for plum in plumage_data:
            serializer = AuthorSerializer(data=plum)
            if serializer.is_valid():
                obj = serializer.save()
                plumage.append(obj)
            else:
                print(serializer.errors)
        instance.plumage.set(plumage)
        lengths_data = validated_data.pop('lengths', [])
        lengths = []
        instance.lengths.all().delete()
        for len in lengths_data:
            serializer = MeasureSerializer(data=len)
            if serializer.is_valid():
                obj = serializer.save()
                lengths.append(obj)
            else:
                print(serializer.errors)
        instance.lengths.set(lengths)
        weights_data = validated_data.pop('weights', [])
        weights = []
        instance.weights.all().delete()
        for wei in weights_data:
            serializer = MeasureSerializer(data=wei)
            if serializer.is_valid():
                obj = serializer.save()
                weights.append(obj)
            else:
                print(serializer.errors)
        instance.weights.set(weights)
        description = validated_data.get('description', None)
        if description:
            serializer = TextSerializer(instance.text, data=description)
            if serializer.is_valid():
                description = serializer.save()
                instance.text = description
            else:
                print(serializer.errors)
        instance.save()
        return instance


class ReproductionSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)
    types = TypeSerializer(required=False, many=True)

    class Meta:
        model = Reproduction
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        types_data = validated_data.pop('types', [])
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        reproduction = Reproduction.objects.create(text=text, **validated_data)
        types = []
        for len in types_data:
            serializer = TypeSerializer(data=len)
            if serializer.is_valid():
                obj = serializer.save()
                types.append(obj)
            else:
                print(serializer.errors)
        reproduction.types.set(types)
        return reproduction

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        types_data = validated_data.get('types', [])
        types = []
        instance.types.all().delete()
        for type in types_data:
            serializer = TypeSerializer(data=type)
            if serializer.is_valid():
                obj = serializer.save()
                types.append(obj)
            else:
                print(serializer.errors)
        instance.types.set(types)
        instance.save()
        return instance


class ReferenceSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False)

    class Meta:
        model = Reference
        exclude = ('id',)

    def create(self, validated_data):
        authors_data = validated_data.pop('authors', [])
        reference = Reference.objects.create(**validated_data)
        authors = []
        for author in authors_data:
            serializer = AuthorSerializer(data=author)
            if serializer.is_valid():
                au = serializer.save()
                authors.append(au)
            else:
                print(serializer.errors)
        reference.authors.set(authors)
        return reference

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', [])
        authors = []
        instance.authors.all().delete()
        for author in authors_data:
            serializer = AuthorSerializer(data=author)
            if serializer.is_valid():
                au = serializer.save()
                authors.append(au)
            else:
                print(serializer.errors)
        instance.authors.set(authors)
        instance.referenced = validated_data.get('referenced', None)
        instance.type = validated_data.get('type', None)
        instance.title = validated_data.get('title', None)
        instance.year = validated_data.get('year', None)
        instance.series = validated_data.get('series', None)
        instance.volume = validated_data.get('volume', None)
        instance.edition = validated_data.get('edition', None)
        instance.isbn = validated_data.get('isbn', None)
        instance.publisher = validated_data.get('publisher', None)
        instance.doi = validated_data.get('doi', None)
        instance.url = validated_data.get('url', None)
        instance.initial_page = validated_data.get('initial_page', None)
        instance.last_page = validated_data.get('last_page', None)
        instance.date_accessed = validated_data.get('date_accessed', None)
        instance.save()
        return instance


class BirdImageSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)

    class Meta:
        model = BirdImage
        exclude = ('id', 'bird')
        extra_kwargs = {
            'url': {'validators': []},
        }

    def create(self, validated_data):
        author = validated_data.pop('author', None)
        if author:
            serializer = AuthorSerializer(data=author)
            if serializer.is_valid():
                author = serializer.save()
            else:
                print(serializer.errors)
        image = BirdImage.objects.create(author=author, **validated_data)
        return image

    def update(self, instance, validated_data):
        author = validated_data.get('author', None)
        if author:
            serializer = AuthorSerializer(instance.author, data=author)
            if serializer.is_valid():
                author = serializer.save()
                instance.author = author
            else:
                print(serializer.errors)
        instance.category = validated_data.get('category', None)
        instance.location = validated_data.get('location', None)
        instance.main = validated_data.get('main', None)
        instance.save()
        return instance


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ('id', 'bird')
        extra_kwargs = {
            'url': {'validators': []},
        }


class AudioSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)

    class Meta:
        model = Audio
        exclude = ('id',)
        extra_kwargs = {
            'url': {'validators': []},
        }

    def create(self, validated_data):
        author = validated_data.pop('author', None)
        if author:
            serializer = AuthorSerializer(data=author)
            if serializer.is_valid():
                author = serializer.save()
            else:
                print(serializer.errors)
        audio = Audio.objects.create(author=author, **validated_data)
        return audio

    def update(self, instance, validated_data):
        author = validated_data.get('author', None)
        if author:
            serializer = ReferenceSerializer(instance.author, data=author)
            if serializer.is_valid():
                author = serializer.save()
                instance.author = author
            else:
                print(serializer.errors)
        instance.url = validated_data.get('url', None)
        instance.format = validated_data.get('format', None)
        instance.location = validated_data.get('location', None)
        instance.save()
        return instance


class VocalizationSerializer(serializers.ModelSerializer):
    short_description = TextSerializer(required=False)
    long_description = TextSerializer(required=False)
    audio = AudioSerializer(required=False)

    class Meta:
        model = Vocalization
        exclude = ('id', 'bird')

    def create(self, validated_data):
        short_description = validated_data.pop('short_description', None)
        if short_description:
            serializer = TextSerializer(data=short_description)
            if serializer.is_valid():
                short_description = serializer.save()
            else:
                print(serializer.errors)
        long_description = validated_data.pop('long_description', None)
        if long_description:
            serializer = TextSerializer(data=long_description)
            if serializer.is_valid():
                long_description = serializer.save()
            else:
                print(serializer.errors)
        audio = validated_data.pop('audio', None)
        if audio:
            serializer = AudioSerializer(data=audio)
            if serializer.is_valid():
                audio = serializer.save()
            else:
                print(serializer.errors)
        vocalization = Vocalization.objects.create(short_description=short_description,
                                                   long_description=long_description, audio=audio, **validated_data)
        return vocalization

    def update(self, instance, validated_data):
        short_description = validated_data.get('short_description', None)
        if short_description:
            serializer = TextSerializer(instance.short_description, data=short_description)
            if serializer.is_valid():
                short_description = serializer.save()
                instance.short_description = short_description
            else:
                print(serializer.errors)
        long_description = validated_data.get('long_description', None)
        if long_description:
            serializer = TextSerializer(instance.long_description, data=long_description)
            if serializer.is_valid():
                long_description = serializer.save()
                instance.long_description = long_description
            else:
                print(serializer.errors)
        audio = validated_data.get('audio', None)
        if audio:
            serializer = AudioSerializer(instance.audio, data=audio)
            if serializer.is_valid():
                audio = serializer.save()
                instance.audio = audio
            else:
                print(serializer.errors)
        instance.category = validated_data.get('category', None)
        instance.save()
        return instance


class SubspeciesNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubspeciesName
        fields = ('name', 'main')


class DistributionSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)
    location_map = ImageSerializer(required=False)

    class Meta:
        model = Distribution
        fields = ('text', 'location_map')

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        location_map = validated_data.pop('location_map', None)
        if location_map:
            serializer = ImageSerializer(data=location_map)
            if serializer.is_valid():
                location_map = serializer.save()
            else:
                print(serializer.errors)
        distribution = Distribution.objects.create(text=text, location_map=location_map)
        return distribution

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.name = text
            else:
                print(serializer.errors)
        location_map = validated_data.get('location_map', None)
        if location_map:
            serializer = ImageSerializer(instance.location_map, data=location_map)
            if serializer.is_valid():
                location_map = serializer.save()
                instance.name = location_map
            else:
                print(serializer.errors)
        instance.save()
        return instance


class SubspeciesSerializer(serializers.ModelSerializer):
    names = SubspeciesNameSerializer(required=False, many=True)
    distribution = DistributionSerializer(required=False)

    class Meta:
        model = Subspecies
        fields = ('names', 'distribution')

    def create(self, validated_data):
        distribution = validated_data.pop('distribution', None)
        if distribution:
            serializer = DistributionSerializer(data=distribution)
            if serializer.is_valid():
                distribution = serializer.save()
            else:
                print(serializer.errors)
        names_data = validated_data.pop('names', [])
        subspecies = Subspecies.objects.create(distribution=distribution)
        names = []
        for name in names_data:
            serializer = SubspeciesNameSerializer(data=name)
            if serializer.is_valid():
                obj = serializer.save()
                names.append(obj)
            else:
                print(serializer.errors)
        subspecies.names.set(names)
        return subspecies

    def update(self, instance, validated_data):
        distribution = validated_data.get('distribution', None)
        if distribution:
            serializer = DistributionSerializer(instance.distribution, data=distribution)
            if serializer.is_valid():
                distribution = serializer.save()
                instance.distribution = distribution
            else:
                print(serializer.errors)
        names_data = validated_data.get('names', [])
        names = []
        instance.names.all().delete()
        for name in names_data:
            serializer = SubspeciesNameSerializer(data=name)
            if serializer.is_valid():
                obj = serializer.save()
                names.append(obj)
            else:
                print(serializer.errors)
        instance.names.set(names)
        instance.save()
        return instance


class BirdSerializer(serializers.ModelSerializer):
    family = PrimaryKeyRelatedField(queryset=Family.objects.all(), required=False)
    subspecies = SubspeciesSerializer(required=False, many=True)
    common_names = CommonNameBirdSerializer(required=False, many=True)
    scientific_names = ScientificNameBirdSerializer(required=False, many=True)
    images = BirdImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)
    vocalizations = VocalizationSerializer(many=True, required=False)
    description = TextSerializer(required=False)
    identification = IdentificationSerializer(required=False)
    distribution = DistributionSerializer(required=False)
    migration = TypeSerializer(required=False)
    habitat = TextSerializer(required=False)
    feeding = TypeSerializer(many=True, required=False)
    reproduction = ReproductionSerializer(required=False)
    behavior = TypeSerializer(many=True, required=False)
    taxonomy = TextSerializer(required=False)
    conservation = TypeSerializer(required=False)
    similar_species = SimilarSpeciesSerializer(required=False)
    references = ReferenceSerializer(required=False, many=True)
    own_citation = ReferenceSerializer(required=False)

    class Meta:
        model = Bird
        fields = '__all__'

    def get_fields(self):
        fields = super(BirdSerializer, self).get_fields()
        return fields

    def create(self, validated_data):
        family = validated_data.pop('family', None)
        description = validated_data.pop('description', None)
        if description:
            description = Text.objects.create(**description)
        identification = validated_data.pop('identification', None)
        if identification:
            serializer = IdentificationSerializer(data=identification)
            if serializer.is_valid():
                identification = serializer.save()
            else:
                print(serializer.errors)
        distribution = validated_data.pop('distribution', None)
        if distribution:
            serializer = DistributionSerializer(data=distribution)
            if serializer.is_valid():
                distribution = serializer.save()
            else:
                print(serializer.errors)
        migration = validated_data.pop('migration', None)
        if migration:
            serializer = TypeSerializer(data=migration)
            if serializer.is_valid():
                migration = serializer.save()
            else:
                print(serializer.errors)
        habitat = validated_data.pop('habitat', None)
        if habitat:
            habitat = Text.objects.create(**habitat)
        reproduction = validated_data.pop('reproduction', None)
        if reproduction:
            serializer = ReproductionSerializer(data=reproduction)
            if serializer.is_valid():
                reproduction = serializer.save()
            else:
                print(serializer.errors)
        taxonomy = validated_data.pop('taxonomy', None)
        if taxonomy:
            taxonomy = Text.objects.create(**taxonomy)
        conservation = validated_data.pop('conservation', None)
        if conservation:
            serializer = TypeSerializer(data=conservation)
            if serializer.is_valid():
                conservation = serializer.save()
            else:
                print(serializer.errors)
        similar_species = validated_data.pop('similar_species', None)
        similar_species['bird_ids'] = [ss.id for ss in similar_species['bird_ids']]
        if similar_species:
            serializer = SimilarSpeciesSerializer(data=similar_species)
            if serializer.is_valid():
                similar_species = serializer.save()
            else:
                print(serializer.errors)
        own_citation = validated_data.pop('own_citation', None)
        if own_citation:
            serializer = ReferenceSerializer(data=own_citation)
            if serializer.is_valid():
                own_citation = serializer.save()
            else:
                print(serializer.errors)
        subspecies_data = validated_data.pop('subspecies', [])
        common_names_data = validated_data.pop('common_names', [])
        scientific_names_data = validated_data.pop('scientific_names', [])
        images_data = validated_data.pop('images', [])
        videos_data = validated_data.pop('videos', [])
        vocalizations_data = validated_data.pop('vocalizations', [])
        feeding_data = validated_data.pop('feeding', [])
        behavior_data = validated_data.pop('behavior', [])
        references_data = validated_data.pop('references', [])
        bird = Bird.objects.create(family=family, description=description, identification=identification,
                                   distribution=distribution, migration=migration, habitat=habitat,
                                   reproduction=reproduction, taxonomy=taxonomy, conservation=conservation,
                                   similar_species=similar_species, own_citation=own_citation, **validated_data)

        subspecies = []
        for subs in subspecies_data:
            serializer = SubspeciesSerializer(data=subs)
            if serializer.is_valid():
                obj = serializer.save()
                subspecies.append(obj)
            else:
                print(serializer.errors)
        bird.subspecies.set(subspecies)
        common_names = []
        for c_n in common_names_data:
            serializer = CommonNameBirdSerializer(data=c_n)
            if serializer.is_valid():
                c_n = serializer.save()
                common_names.append(c_n)
            else:
                print(serializer.errors)
        bird.common_names.set(common_names)
        scientific_names = []
        for sci_name in scientific_names_data:
            serializer = ScientificNameBirdSerializer(data=sci_name)
            if serializer.is_valid():
                c_n = serializer.save()
                scientific_names.append(c_n)
            else:
                print(serializer.errors)
        bird.scientific_names.set(scientific_names)
        images = []
        for image in images_data:
            serializer = BirdImageSerializer(data=image)
            if serializer.is_valid():
                im = serializer.save()
                images.append(im)
            else:
                print(serializer.errors)
        bird.images.set(images)
        videos = []
        for video in videos_data:
            serializer = VideoSerializer(data=video)
            if serializer.is_valid():
                vid = serializer.save()
                videos.append(vid)
            else:
                print(serializer.errors)
        bird.videos.set(videos)
        vocalizations = []
        for song in vocalizations_data:
            serializer = VocalizationSerializer(data=song)
            if serializer.is_valid():
                si = serializer.save()
                vocalizations.append(si)
            else:
                print(serializer.errors)
        bird.vocalizations.set(vocalizations)
        feeding = []
        for feed in feeding_data:
            serializer = TypeSerializer(data=feed)
            if serializer.is_valid():
                obj = serializer.save()
                feeding.append(obj)
            else:
                print(serializer.errors)
        bird.feeding.set(feeding)
        behavior = []
        for beh in behavior_data:
            serializer = TypeSerializer(data=beh)
            if serializer.is_valid():
                obj = serializer.save()
                behavior.append(obj)
            else:
                print(serializer.errors)
        bird.behavior.set(behavior)
        references = []
        for ref in references_data:
            serializer = ReferenceSerializer(data=ref)
            if serializer.is_valid():
                obj = serializer.save()
                references.append(obj)
            else:
                print(serializer.errors)
        bird.references.set(references)
        return bird

    def update(self, instance, validated_data):
        family = validated_data.pop('family', None)
        if family:
            instance.family = family
        description = validated_data.pop('description', None)
        if description:
            serializer = TextSerializer(instance.description, data=description)
            if serializer.is_valid():
                description = serializer.save()
                instance.description = description
            else:
                print(serializer.errors)
        identification = validated_data.pop('identification', None)
        if identification:
            serializer = IdentificationSerializer(instance.identification, data=identification)
            if serializer.is_valid():
                identification = serializer.save()
                instance.identification = identification
            else:
                print(serializer.errors)
        distribution = validated_data.pop('distribution', None)
        if distribution:
            serializer = DistributionSerializer(instance.distribution, data=distribution)
            if serializer.is_valid():
                distribution = serializer.save()
                instance.distribution = distribution
            else:
                print(serializer.errors)
        migration = validated_data.pop('migration', None)
        if migration:
            serializer = TypeSerializer(instance.migration, data=migration)
            if serializer.is_valid():
                migration = serializer.save()
                instance.migration = migration
            else:
                print(serializer.errors)
        habitat = validated_data.pop('habitat', None)
        if habitat:
            serializer = TextSerializer(instance.habitat, data=habitat)
            if serializer.is_valid():
                habitat = serializer.save()
                instance.habitat = habitat
            else:
                print(serializer.errors)
        reproduction = validated_data.pop('reproduction', None)
        if reproduction:
            serializer = ReproductionSerializer(instance.reproduction, data=reproduction)
            if serializer.is_valid():
                reproduction = serializer.save()
                instance.reproduction = reproduction
            else:
                print(serializer.errors)
        taxonomy = validated_data.pop('taxonomy', None)
        if taxonomy:
            serializer = TextSerializer(instance.taxonomy, data=taxonomy)
            if serializer.is_valid():
                taxonomy = serializer.save()
                instance.taxonomy = taxonomy
            else:
                print(serializer.errors)
        conservation = validated_data.pop('conservation', None)
        if conservation:
            serializer = TypeSerializer(instance.conservation, data=conservation)
            if serializer.is_valid():
                conservation = serializer.save()
                instance.conservation = conservation
            else:
                print(serializer.errors)
        similar_species = validated_data.pop('similar_species', None)
        if similar_species:
            serializer = SimilarSpeciesSerializer(instance.similar_species, data=similar_species)
            if serializer.is_valid():
                similar_species = serializer.save()
                instance.similar_species = similar_species
            else:
                print(serializer.errors)
        own_citation = validated_data.pop('own_citation', None)
        if own_citation:
            serializer = ReferenceSerializer(instance.own_citation, data=own_citation)
            if serializer.is_valid():
                own_citation = serializer.save()
                instance.own_citation = own_citation
            else:
                print(serializer.errors)

        instance.subspecies.all().delete()
        subspecies_data = validated_data.pop('subspecies', [])
        subspecies = []
        for subs in subspecies_data:
            serializer = SubspeciesSerializer(data=subs)
            if serializer.is_valid():
                obj = serializer.save()
                subspecies.append(obj)
            else:
                print(serializer.errors)
        instance.subspecies.set(subspecies)
        instance.common_names.all().delete()
        common_names_data = validated_data.pop('common_names', [])
        common_names = []
        for com_name in common_names_data:
            serializer = CommonNameBirdSerializer(data=com_name)
            if serializer.is_valid():
                obj = serializer.save()
                common_names.append(obj)
            else:
                print(serializer.errors)
        instance.common_names.set(common_names)
        instance.scientific_names.all().delete()
        scientific_names_data = validated_data.pop('scientific_names', [])
        scientific_names = []
        for sci_name in scientific_names_data:
            serializer = ScientificNameBirdSerializer(data=sci_name)
            if serializer.is_valid():
                si = serializer.save()
                scientific_names.append(si)
            else:
                print(serializer.errors)
        instance.scientific_names.set(scientific_names)
        instance.images.all().delete()
        images_data = validated_data.pop('images', [])
        images = []
        for image in images_data:
            serializer = BirdImageSerializer(data=image)
            if serializer.is_valid():
                si = serializer.save()
                images.append(si)
            else:
                print(serializer.errors)
        instance.images.set(images)
        instance.videos.all().delete()
        videos_data = validated_data.pop('videos', [])
        videos = []
        for video in videos_data:
            serializer = VideoSerializer(data=video)
            if serializer.is_valid():
                si = serializer.save()
                videos.append(si)
            else:
                print(serializer.errors)
        instance.videos.set(videos)
        instance.vocalizations.all().delete()
        vocalizations_data = validated_data.pop('vocalizations', [])
        vocalizations = []
        for song in vocalizations_data:
            serializer = VocalizationSerializer(data=song)
            if serializer.is_valid():
                obj = serializer.save()
                vocalizations.append(obj)
            else:
                print(serializer.errors)
        instance.vocalizations.set(vocalizations)
        instance.feeding.all().delete()
        feeding_data = validated_data.pop('feeding', [])
        feeding = []
        for feed in feeding_data:
            serializer = TypeSerializer(data=feed)
            if serializer.is_valid():
                obj = serializer.save()
                feeding.append(obj)
            else:
                print(serializer.errors)
        instance.feeding.set(feeding)
        instance.behavior.all().delete()
        behavior_data = validated_data.pop('behavior', [])
        behavior = []
        for beh in behavior_data:
            serializer = TypeSerializer(data=beh)
            if serializer.is_valid():
                obj = serializer.save()
                behavior.append(obj)
            else:
                print(serializer.errors)
        instance.behavior.set(behavior)
        instance.references.all().delete()
        references_data = validated_data.pop('references', [])
        references = []
        for ref in references_data:
            serializer = ReferenceSerializer(data=ref)
            if serializer.is_valid():
                obj = serializer.save()
                references.append(obj)
            else:
                print(serializer.errors)
        instance.references.set(references)
        instance.save()
        return instance



