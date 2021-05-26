from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from birds.models import Text, Author, Image, ScientificNameOrder, ScientificNameFamily, CommonNameBird, \
    ScientificNameBird, Order, Family, Identification, Type, Measure, Value, Reference, Bird, Video, \
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
    image = ImageSerializer(required=False, allow_null=True)
    description = TextSerializer(required=False, allow_null=True)

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
        description = validated_data.pop('description', None)
        if description:
            serializer = TextSerializer(data=description)
            if serializer.is_valid():
                description = serializer.save()
            else:
                print(serializer.errors)
        author = Author.objects.create(image=image, description=description, **validated_data)
        return author

    def update(self, instance, validated_data):
        image = validated_data.get('image', "")
        if image != "":
            if image:
                serializer = ImageSerializer(instance.image, data=image)
                if serializer.is_valid():
                    image = serializer.save()
                    instance.image = image
                else:
                    print(serializer.errors)
            else:
                instance.image = None
        description = validated_data.get('description', "")
        if description != "":
            if description:
                serializer = ImageSerializer(instance.description, data=description)
                if serializer.is_valid():
                    description = serializer.save()
                    instance.description = description
                else:
                    print(serializer.errors)
            else:
                instance.description = None
        first_name = validated_data.get('first_name', "")
        if first_name != "":
            instance.first_name = first_name
        last_name = validated_data.get('last_name', "")
        if last_name != "":
            instance.last_name = last_name
        url = validated_data.get('url', "")
        if url != "":
            instance.url = url
        description = validated_data.get('description', "")
        if description != "":
            instance.description = description
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
    text = TextSerializer(required=False, allow_null=True)
    bird_ids = PrimaryKeyRelatedField(many=True, queryset=Bird.objects.all(), required=False, allow_null=True)

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
            bird_ids.append(ss)
        obj = SimilarSpecies.objects.create(text=text)
        obj.bird_ids.set(bird_ids)
        return obj

    def update(self, instance, validated_data):
        text = validated_data.get('text', "")
        if text != "":
            if text:
                serializer = TextSerializer(instance.text, data=text)
                if serializer.is_valid():
                    text = serializer.save()
                    instance.text = text
                else:
                    print(serializer.errors)
            else:
                instance.text = None
        similar_species_data = validated_data.pop('bird_ids', [])
        bird_ids = []
        for ss in similar_species_data:
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
        scientific_names_data = validated_data.get('scientific_names', None)
        if scientific_names_data:
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
        scientific_names_data = validated_data.get('scientific_names', None)
        if scientific_names_data:
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
    name = TextSerializer(required=False, allow_null=True)
    image = ImageSerializer(required=False, allow_null=True)
    text = TextSerializer(required=False, allow_null=True)

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
        name = validated_data.get('name', "")
        if name != "":
            if name:
                serializer = TextSerializer(instance.name, data=name)
                if serializer.is_valid():
                    name = serializer.save()
                    instance.name = name
                else:
                    print(serializer.errors)
            else:
                instance.name = None
        image = validated_data.get('image', "")
        if image != "":
            if image:
                serializer = ImageSerializer(instance.image, data=image)
                if serializer.is_valid():
                    image = serializer.save()
                    instance.image = image
                else:
                    print(serializer.errors)
            else:
                instance.image = None
        text = validated_data.get('text', "")
        if text != "":
            if text:
                serializer = TextSerializer(instance.text, data=text)
                if serializer.is_valid():
                    text = serializer.save()
                    instance.text = text
                else:
                    print(serializer.errors)
            else:
                instance.text = None
        instance.save()
        return instance


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        exclude = ('id',)


class ReferenceSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False, allow_null=True)

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
        authors_data = validated_data.pop('authors', None)
        if authors_data:
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
        referenced = validated_data.get('referenced', "")
        if referenced != "":
            instance.referenced = referenced
        type = validated_data.get('type', "")
        if type != "":
            instance.type = type
        title = validated_data.get('title', "")
        if title != "":
            instance.title = title
        year = validated_data.get('year', "")
        if year != "":
            instance.year = year
        series = validated_data.get('series', "")
        if series != "":
            instance.series = series
        volume = validated_data.get('volume', "")
        if volume != "":
            instance.volume = volume
        edition = validated_data.get('edition', "")
        if edition != "":
            instance.edition = edition
        isbn = validated_data.get('isbn', "")
        if isbn != "":
            instance.isbn = isbn
        publisher = validated_data.get('publisher', "")
        if publisher != "":
            instance.publisher = publisher
        doi = validated_data.get('doi', "")
        if doi != "":
            instance.doi = doi
        url = validated_data.get('url', "")
        if url != "":
            instance.url = url
        initial_page = validated_data.get('initial_page', "")
        if initial_page != "":
            instance.initial_page = initial_page
        last_page = validated_data.get('last_page', "")
        if last_page != "":
            instance.last_page = last_page
        date_accessed = validated_data.get('date_accessed', "")
        if date_accessed != "":
            instance.date_accessed = date_accessed
        instance.save()
        return instance


class MeasureSerializer(serializers.ModelSerializer):
    value = ValueSerializer(required=False)
    reference = ReferenceSerializer(required=False, allow_null=True)

    class Meta:
        model = Measure
        fields = ('value', 'unit', 'name', 'reference')

    def create(self, validated_data):
        value = validated_data.pop('value', None)
        if value:
            serializer = ValueSerializer(data=value)
            if serializer.is_valid():
                value = serializer.save()
            else:
                print(serializer.errors)
        reference = validated_data.pop('reference', None)
        if reference:
            serializer = ReferenceSerializer(data=reference)
            if serializer.is_valid():
                reference = serializer.save()
            else:
                print(serializer.errors)
        measure = Measure.objects.create(value=value, reference=reference, **validated_data)
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
        reference = validated_data.get('reference', "")
        if reference != "":
            if reference:
                serializer = ReferenceSerializer(instance.reference, data=reference)
                if serializer.is_valid():
                    reference = serializer.save()
                    instance.reference = reference
                else:
                    print(serializer.errors)
            else:
                instance.reference = None
        instance.name = validated_data.get('name', None)
        instance.unit = validated_data.get('unit', None)
        instance.save()
        return instance


class IdentificationSerializer(serializers.ModelSerializer):
    description = TextSerializer(required=False, allow_null=True)
    plumage = TypeSerializer(required=False, allow_null=True, many=True)
    lengths = MeasureSerializer(required=False, allow_null=True, many=True)
    weights = MeasureSerializer(required=False, allow_null=True, many=True)

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
        plumage_data = validated_data.pop('plumage', None)
        if plumage_data:
            plumage = []
            instance.plumage.all().delete()
            for plum in plumage_data:
                serializer = TypeSerializer(data=plum)
                if serializer.is_valid():
                    obj = serializer.save()
                    plumage.append(obj)
                else:
                    print(serializer.errors)
            instance.plumage.set(plumage)
        lengths_data = validated_data.pop('lengths', None)
        if lengths_data:
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
        weights_data = validated_data.pop('weights', None)
        if weights_data:
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
        description = validated_data.get('description', "")
        if description != "":
            if description:
                serializer = TextSerializer(instance.description, data=description)
                if serializer.is_valid():
                    description = serializer.save()
                    instance.description = description
                else:
                    print(serializer.errors)
            else:
                instance.description = None
        instance.save()
        return instance


class BirdImageSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False, allow_null=True)

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
        author = validated_data.get('author', "")
        if author != "":
            if author:
                serializer = AuthorSerializer(instance.author, data=author)
                if serializer.is_valid():
                    author = serializer.save()
                    instance.author = author
                else:
                    print(serializer.errors)
            else:
                instance.author = None
        category = validated_data.get('category', "")
        if category != "":
            instance.category = category
        location = validated_data.get('location', "")
        if location != "":
            instance.location = location
        main = validated_data.get('main', "")
        if main != "":
            instance.main = main
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
    author = AuthorSerializer(required=False, allow_null=True)

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
        author = validated_data.get('author', "")
        if author != "":
            if author:
                serializer = ReferenceSerializer(instance.author, data=author)
                if serializer.is_valid():
                    author = serializer.save()
                    instance.author = author
                else:
                    print(serializer.errors)
            else:
                instance.author = None
        url = validated_data.get('url', "")
        if url != "":
            instance.url = url
        format = validated_data.get('format', "")
        if format != "":
            instance.format = format
        location = validated_data.get('location', "")
        if location != "":
            instance.location = location
        instance.save()
        return instance


class VocalizationSerializer(serializers.ModelSerializer):
    short_description = TextSerializer(required=False, allow_null=True)
    long_description = TextSerializer(required=False, allow_null=True)
    audio = AudioSerializer(required=False, allow_null=True)

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
        short_description = validated_data.get('short_description', "")
        if short_description != "":
            if short_description:
                serializer = TextSerializer(instance.short_description, data=short_description)
                if serializer.is_valid():
                    short_description = serializer.save()
                    instance.short_description = short_description
                else:
                    print(serializer.errors)
            else:
                instance.short_description = None
        long_description = validated_data.get('long_description', "")
        if long_description != "":
            if long_description:
                serializer = TextSerializer(instance.long_description, data=long_description)
                if serializer.is_valid():
                    long_description = serializer.save()
                    instance.long_description = long_description
                else:
                    print(serializer.errors)
            else:
                instance.long_description = None
        audio = validated_data.get('audio', "")
        if audio != "":
            if audio:
                serializer = AudioSerializer(instance.audio, data=audio)
                if serializer.is_valid():
                    audio = serializer.save()
                    instance.audio = audio
                else:
                    print(serializer.errors)
            else:
                instance.audio = None
        category = validated_data.get('category', "")
        if category != "":
            instance.category = category
        instance.save()
        return instance


class SubspeciesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubspeciesName
        fields = ('name', 'main')


class DistributionSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False, allow_null=True)
    location_map = ImageSerializer(required=False, allow_null=True)

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
        text = validated_data.get('text', "")
        if text != "":
            if text:
                serializer = TextSerializer(instance.text, data=text)
                if serializer.is_valid():
                    text = serializer.save()
                    instance.text = text
                else:
                    print(serializer.errors)
            else:
                instance.text = None
        location_map = validated_data.get('location_map', "")
        if location_map != "":
            if location_map:
                serializer = ImageSerializer(instance.location_map, data=location_map)
                if serializer.is_valid():
                    location_map = serializer.save()
                    instance.location_map = location_map
                else:
                    print(serializer.errors)
            else:
                instance.location_map = None
        instance.save()
        return instance


class SubspeciesSerializer(serializers.ModelSerializer):
    names = SubspeciesNameSerializer(required=False, allow_null=True, many=True)
    distribution = DistributionSerializer(required=False, allow_null=True)
    images = BirdImageSerializer(many=True, required=False, allow_null=True)
    lengths = MeasureSerializer(required=False, allow_null=True, many=True)
    weights = MeasureSerializer(required=False, allow_null=True, many=True)

    class Meta:
        model = Subspecies
        fields = ('names', 'distribution', 'images', 'lengths', 'weights')

    def create(self, validated_data):
        distribution = validated_data.pop('distribution', None)
        if distribution:
            serializer = DistributionSerializer(data=distribution)
            if serializer.is_valid():
                distribution = serializer.save()
            else:
                print(serializer.errors)
        names_data = validated_data.pop('names', [])
        images_data = validated_data.pop('images', [])
        lengths_data = validated_data.pop('lengths', [])
        weights_data = validated_data.pop('weights', [])
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
        images = []
        for image in images_data:
            serializer = BirdImageSerializer(data=image)
            if serializer.is_valid():
                im = serializer.save()
                images.append(im)
            else:
                print(serializer.errors)
        subspecies.images.set(images)
        lengths = []
        for len in lengths_data:
            serializer = MeasureSerializer(data=len)
            if serializer.is_valid():
                obj = serializer.save()
                lengths.append(obj)
            else:
                print(serializer.errors)
        subspecies.lengths.set(lengths)
        weights = []
        for wei in weights_data:
            serializer = MeasureSerializer(data=wei)
            if serializer.is_valid():
                obj = serializer.save()
                weights.append(obj)
            else:
                print(serializer.errors)
        subspecies.weights.set(weights)
        return subspecies

    def update(self, instance, validated_data):
        distribution = validated_data.get('distribution', "")
        if distribution != "":
            if distribution:
                serializer = DistributionSerializer(instance.distribution, data=distribution)
                if serializer.is_valid():
                    distribution = serializer.save()
                    instance.distribution = distribution
                else:
                    print(serializer.errors)
            else:
                instance.distribution = None
        names_data = validated_data.get('names', None)
        if names_data:
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
        images_data = validated_data.pop('images', None)
        if images_data:
            instance.images.all().delete()
            images = []
            for image in images_data:
                serializer = BirdImageSerializer(data=image)
                if serializer.is_valid():
                    si = serializer.save()
                    images.append(si)
                else:
                    print(serializer.errors)
            instance.images.set(images)
        lengths_data = validated_data.pop('lengths', None)
        if lengths_data:
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
        weights_data = validated_data.pop('weights', None)
        if weights_data:
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
        instance.save()
        return instance


class BirdSerializer(serializers.ModelSerializer):
    family = PrimaryKeyRelatedField(queryset=Family.objects.all(), required=False)
    subspecies = SubspeciesSerializer(required=False, allow_null=True, many=True)
    common_names = CommonNameBirdSerializer(required=False, allow_null=True, many=True)
    scientific_names = ScientificNameBirdSerializer(required=False, many=True)
    images = BirdImageSerializer(many=True, required=False, allow_null=True)
    videos = VideoSerializer(many=True, required=False, allow_null=True)
    vocalizations = VocalizationSerializer(many=True, required=False, allow_null=True)
    description = TextSerializer(required=False, allow_null=True)
    identification = IdentificationSerializer(required=False, allow_null=True)
    distribution = DistributionSerializer(required=False, allow_null=True)
    migration = TypeSerializer(required=False, allow_null=True)
    habitat = TextSerializer(required=False, allow_null=True)
    feeding = TypeSerializer(many=True, required=False, allow_null=True)
    reproduction = TypeSerializer(required=False, allow_null=True, many=True)
    behavior = TypeSerializer(many=True, required=False, allow_null=True)
    taxonomy = TextSerializer(required=False, allow_null=True)
    conservation = TypeSerializer(required=False, allow_null=True)
    similar_species = SimilarSpeciesSerializer(required=False, allow_null=True)
    references = ReferenceSerializer(required=False, allow_null=True, many=True)
    own_citation = ReferenceSerializer(required=False, allow_null=True)
    authors = PrimaryKeyRelatedField(many=True, queryset=Author.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Bird
        exclude = ('similar_species_class_id', )

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
        if similar_species:
            similar_species['bird_ids'] = [ss.id for ss in similar_species['bird_ids']]
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
        reproduction_data = validated_data.pop('reproduction', [])
        behavior_data = validated_data.pop('behavior', [])
        references_data = validated_data.pop('references', [])
        authors_data = validated_data.pop('authors', [])
        bird = Bird.objects.create(family=family, description=description, identification=identification,
                                   distribution=distribution, migration=migration, habitat=habitat,
                                   taxonomy=taxonomy, conservation=conservation,
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
        reproduction = []
        for repr in reproduction_data:
            serializer = TypeSerializer(data=repr)
            if serializer.is_valid():
                obj = serializer.save()
                reproduction.append(obj)
            else:
                print(serializer.errors)
        bird.reproduction.set(reproduction)
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
        authors = []
        for au in authors_data:
            authors.append(au)
        bird.authors.set(authors)
        return bird

    def update(self, instance, validated_data):
        family = validated_data.pop('family', None)
        if family:
            instance.family = family
        description = validated_data.pop('description', "")
        if description != "":
            if description:
                serializer = TextSerializer(instance.description, data=description)
                if serializer.is_valid():
                    description = serializer.save()
                    instance.description = description
                else:
                    print(serializer.errors)
            else:
                instance.description = None
        identification = validated_data.pop('identification', "")
        if identification != "":
            if identification:
                serializer = IdentificationSerializer(instance.identification, data=identification)
                if serializer.is_valid():
                    identification = serializer.save()
                    instance.identification = identification
                else:
                    print(serializer.errors)
            else:
                instance.identification = None
        distribution = validated_data.pop('distribution', "")
        if distribution != "":
            if distribution:
                serializer = DistributionSerializer(instance.distribution, data=distribution)
                if serializer.is_valid():
                    distribution = serializer.save()
                    instance.distribution = distribution
                else:
                    print(serializer.errors)
            else:
                instance.distribution = None
        migration = validated_data.pop('migration', "")
        if migration != "":
            if migration:
                serializer = TypeSerializer(instance.migration, data=migration)
                if serializer.is_valid():
                    migration = serializer.save()
                    instance.migration = migration
                else:
                    print(serializer.errors)
            else:
                instance.migration = None
        habitat = validated_data.pop('habitat', "")
        if habitat != "":
            if habitat:
                serializer = TextSerializer(instance.habitat, data=habitat)
                if serializer.is_valid():
                    habitat = serializer.save()
                    instance.habitat = habitat
                else:
                    print(serializer.errors)
            else:
                instance.habitat = None
        taxonomy = validated_data.pop('taxonomy', "")
        if taxonomy != "":
            if taxonomy:
                serializer = TextSerializer(instance.taxonomy, data=taxonomy)
                if serializer.is_valid():
                    taxonomy = serializer.save()
                    instance.taxonomy = taxonomy
                else:
                    print(serializer.errors)
            else:
                instance.taxonomy = None
        conservation = validated_data.pop('conservation', "")
        if conservation != "":
            if conservation:
                serializer = TypeSerializer(instance.conservation, data=conservation)
                if serializer.is_valid():
                    conservation = serializer.save()
                    instance.conservation = conservation
                else:
                    print(serializer.errors)
            else:
                instance.conservation = None
        similar_species = validated_data.pop('similar_species', "")
        if similar_species != "":
            if similar_species:
                similar_species['bird_ids'] = [ss.id for ss in similar_species['bird_ids']]
                serializer = SimilarSpeciesSerializer(instance.similar_species, data=similar_species)
                if serializer.is_valid():
                    similar_species = serializer.save()
                    instance.similar_species = similar_species
                else:
                    print(serializer.errors)
            else:
                instance.similar_species = None
        own_citation = validated_data.pop('own_citation', "")
        if own_citation != "":
            if own_citation:
                serializer = ReferenceSerializer(instance.own_citation, data=own_citation)
                if serializer.is_valid():
                    own_citation = serializer.save()
                    instance.own_citation = own_citation
                else:
                    print(serializer.errors)
            else:
                instance.own_citation = None

        subspecies_data = validated_data.pop('subspecies', None)
        if subspecies_data:
            subspecies = []
            instance.subspecies.all().delete()
            for subs in subspecies_data:
                serializer = SubspeciesSerializer(data=subs)
                if serializer.is_valid():
                    obj = serializer.save()
                    subspecies.append(obj)
                else:
                    print(serializer.errors)
            instance.subspecies.set(subspecies)
        common_names_data = validated_data.pop('common_names', None)
        if common_names_data:
            common_names = []
            instance.common_names.all().delete()
            for com_name in common_names_data:
                serializer = CommonNameBirdSerializer(data=com_name)
                if serializer.is_valid():
                    obj = serializer.save()
                    common_names.append(obj)
                else:
                    print(serializer.errors)
            instance.common_names.set(common_names)
        scientific_names_data = validated_data.pop('scientific_names', None)
        if scientific_names_data:
            scientific_names = []
            instance.scientific_names.all().delete()
            for sci_name in scientific_names_data:
                serializer = ScientificNameBirdSerializer(data=sci_name)
                if serializer.is_valid():
                    si = serializer.save()
                    scientific_names.append(si)
                else:
                    print(serializer.errors)
            instance.scientific_names.set(scientific_names)
        images_data = validated_data.pop('images', None)
        if images_data:
            images = []
            instance.images.all().delete()
            for image in images_data:
                serializer = BirdImageSerializer(data=image)
                if serializer.is_valid():
                    si = serializer.save()
                    images.append(si)
                else:
                    print(serializer.errors)
            instance.images.set(images)
        videos_data = validated_data.pop('videos', None)
        if videos_data:
            videos = []
            instance.videos.all().delete()
            for video in videos_data:
                serializer = VideoSerializer(data=video)
                if serializer.is_valid():
                    si = serializer.save()
                    videos.append(si)
                else:
                    print(serializer.errors)
            instance.videos.set(videos)
        vocalizations_data = validated_data.pop('vocalizations', None)
        if vocalizations_data:
            vocalizations = []
            instance.vocalizations.all().delete()
            for song in vocalizations_data:
                serializer = VocalizationSerializer(data=song)
                if serializer.is_valid():
                    obj = serializer.save()
                    vocalizations.append(obj)
                else:
                    print(serializer.errors)
            instance.vocalizations.set(vocalizations)
        feeding_data = validated_data.pop('feeding', [])
        if feeding_data:
            feeding = []
            instance.feeding.all().delete()
            for feed in feeding_data:
                serializer = TypeSerializer(data=feed)
                if serializer.is_valid():
                    obj = serializer.save()
                    feeding.append(obj)
                else:
                    print(serializer.errors)
            instance.feeding.set(feeding)
        reproduction_data = validated_data.pop('reproduction', [])
        if reproduction_data:
            reproduction = []
            instance.reproduction.all().delete()
            for repr in reproduction_data:
                serializer = TypeSerializer(data=repr)
                if serializer.is_valid():
                    obj = serializer.save()
                    reproduction.append(obj)
                else:
                    print(serializer.errors)
            instance.reproduction.set(reproduction)
        behavior_data = validated_data.pop('behavior', [])
        if behavior_data:
            behavior = []
            instance.behavior.all().delete()
            for beh in behavior_data:
                serializer = TypeSerializer(data=beh)
                if serializer.is_valid():
                    obj = serializer.save()
                    behavior.append(obj)
                else:
                    print(serializer.errors)
            instance.behavior.set(behavior)
        references_data = validated_data.pop('references', [])
        if references_data:
            references = []
            instance.references.all().delete()
            for ref in references_data:
                serializer = ReferenceSerializer(data=ref)
                if serializer.is_valid():
                    obj = serializer.save()
                    references.append(obj)
                else:
                    print(serializer.errors)
            instance.references.set(references)
        authors_data = validated_data.pop('authors', [])
        authors = []
        for au in authors_data:
            authors.append(au)
        instance.authors.set(authors)

        draft_data = validated_data.pop('draft', None)
        if draft_data:
            instance.draft = draft_data

        instance.save()
        return instance
