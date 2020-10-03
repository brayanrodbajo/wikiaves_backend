from rest_framework import serializers

from birds.models import Bird, Text, Family, Identification, Habitat, Feeding, Reproduction, Conservation, Reference, \
    Author, Image, Video, Audio, Length, Order, SDYouth, SDSubadult, SDFemale, SDMale, SexualDifferentiation, \
    ScientificNameOrder, ScientificNameFamily, CommonNameBird, ScientificNameBird


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ('id',)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ('id', 'reference')


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


class ScientificNameBirdSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScientificNameBird
        fields = ('name', 'main')


class OrderSerializer(serializers.ModelSerializer):
    scientific_names = ScientificNameOrderSerializer(required=False, many=True)

    class Meta:
        model = Order
        exclude = ('id',)

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
    order = OrderSerializer(required=False)

    class Meta:
        model = Family
        exclude = ('id',)

    def create(self, validated_data):
        order = validated_data.pop('order', None)
        if order:
            serializer = OrderSerializer(data=order)
            if serializer.is_valid():
                order = serializer.save()
            else:
                print(serializer.errors)
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
            serializer = OrderSerializer(instance.order, data=order)
            if serializer.is_valid():
                order = serializer.save()
                instance.order = order
            else:
                print(serializer.errors)
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


class IdentificationSerializer(serializers.ModelSerializer):
    size_shape = TextSerializer(required=False)
    similar_species = TextSerializer(required=False)
    regional_differences = TextSerializer(required=False)

    class Meta:
        model = Identification
        exclude = ('id',)

    def create(self, validated_data):
        size_shape = validated_data.pop('size_shape', None)
        if size_shape:
            serializer = TextSerializer(data=size_shape)
            if serializer.is_valid():
                size_shape = serializer.save()
            else:
                print(serializer.errors)
        similar_species = validated_data.pop('similar_species', None)
        if similar_species:
            serializer = TextSerializer(data=similar_species)
            if serializer.is_valid():
                similar_species = serializer.save()
            else:
                print(serializer.errors)
        regional_differences = validated_data.pop('regional_differences', None)
        if regional_differences:
            serializer = TextSerializer(data=regional_differences)
            if serializer.is_valid():
                regional_differences = serializer.save()
            else:
                print(serializer.errors)
        identification = Identification.objects.create(size_shape=size_shape, similar_species=similar_species,
                                                       regional_differences=regional_differences)
        return identification

    def update(self, instance, validated_data):
        size_shape = validated_data.get('size_shape', None)
        if size_shape:
            serializer = TextSerializer(instance.size_shape, data=size_shape)
            if serializer.is_valid():
                size_shape = serializer.save()
                instance.size_shape = size_shape
            else:
                print(serializer.errors)
        similar_species = validated_data.get('similar_species', None)
        if similar_species:
            serializer = TextSerializer(instance.similar_species, data=similar_species)
            if serializer.is_valid():
                similar_species = serializer.save()
                instance.similar_species = similar_species
            else:
                print(serializer.errors)
        regional_differences = validated_data.get('regional_differences', None)
        if regional_differences:
            serializer = TextSerializer(instance.regional_differences, data=regional_differences)
            if serializer.is_valid():
                regional_differences = serializer.save()
                instance.regional_differences = regional_differences
            else:
                print(serializer.errors)
        instance.save()
        return instance


class HabitatSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)

    class Meta:
        model = Habitat
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        habitat = Habitat.objects.create(text=text, **validated_data)
        return habitat

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        instance.type = validated_data.get('type', None)
        instance.save()
        return instance


class FeedingSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)

    class Meta:
        model = Feeding
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        feeding = Feeding.objects.create(text=text, **validated_data)
        return feeding

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        instance.type = validated_data.get('type', None)
        instance.save()
        return instance


class ReproductionSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)

    class Meta:
        model = Reproduction
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        reproduction = Reproduction.objects.create(text=text, **validated_data)
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
        instance.type = validated_data.get('type', None)
        instance.save()
        return instance


class ConservationSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)

    class Meta:
        model = Conservation
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        conservation = Conservation.objects.create(text=text, **validated_data)
        return conservation

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        instance.type = validated_data.get('type', None)
        instance.save()
        return instance


class ReferenceSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False)

    class Meta:
        model = Reference
        exclude = ('id',)

    def create(self, validated_data):
        authors_data = validated_data.pop('authors', [])
        reference = Bird.objects.create(**validated_data)
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
        instance.author.all().delete()
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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ('id', 'bird')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ('id', 'bird')


class AudioSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)

    class Meta:
        model = Audio
        exclude = ('id', 'bird')

    def create(self, validated_data):
        author = validated_data.pop('author', None)
        if author:
            serializer = ReferenceSerializer(data=author)
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


class SDYouthSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False)
    text = TextSerializer(required=False)

    class Meta:
        model = SDYouth
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        image = validated_data.pop('image', None)
        if image:
            serializer = ImageSerializer(data=image)
            if serializer.is_valid():
                image = serializer.save()
            else:
                print(serializer.errors)
        sdyouth = SDYouth.objects.create(text=text, image=image)
        return sdyouth

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        image = validated_data.get('image', None)
        if image:
            serializer = ImageSerializer(instance.image, data=image)
            if serializer.is_valid():
                image = serializer.save()
                instance.image = image
            else:
                print(serializer.errors)
        instance.save()
        return instance


class SDSubadultSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False)
    text = TextSerializer(required=False)

    class Meta:
        model = SDSubadult
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        image = validated_data.pop('image', None)
        if image:
            serializer = ImageSerializer(data=image)
            if serializer.is_valid():
                image = serializer.save()
            else:
                print(serializer.errors)
        sdsubadult = SDSubadult.objects.create(text=text, image=image)
        return sdsubadult

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        image = validated_data.get('image', None)
        if image:
            serializer = ImageSerializer(instance.image, data=image)
            if serializer.is_valid():
                image = serializer.save()
                instance.image = image
            else:
                print(serializer.errors)
        instance.save()
        return instance


class SDFemaleSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False)
    text = TextSerializer(required=False)

    class Meta:
        model = SDFemale
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        image = validated_data.pop('image', None)
        if image:
            serializer = ImageSerializer(data=image)
            if serializer.is_valid():
                image = serializer.save()
            else:
                print(serializer.errors)
        sdfemale = SDFemale.objects.create(text=text, image=image)
        return sdfemale

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        image = validated_data.get('image', None)
        if image:
            serializer = ImageSerializer(instance.image, data=image)
            if serializer.is_valid():
                image = serializer.save()
                instance.image = image
            else:
                print(serializer.errors)
        instance.save()
        return instance


class SDMaleSerializer(serializers.ModelSerializer):
    image = ImageSerializer(required=False)
    text = TextSerializer(required=False)

    class Meta:
        model = SDMale
        exclude = ('id',)

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        if text:
            serializer = TextSerializer(data=text)
            if serializer.is_valid():
                text = serializer.save()
            else:
                print(serializer.errors)
        image = validated_data.pop('image', None)
        if image:
            serializer = ImageSerializer(data=image)
            if serializer.is_valid():
                image = serializer.save()
            else:
                print(serializer.errors)
        sdmale = SDMale.objects.create(text=text, image=image)
        return sdmale

    def update(self, instance, validated_data):
        text = validated_data.get('text', None)
        if text:
            serializer = TextSerializer(instance.text, data=text)
            if serializer.is_valid():
                text = serializer.save()
                instance.text = text
            else:
                print(serializer.errors)
        image = validated_data.get('image', None)
        if image:
            serializer = ImageSerializer(instance.image, data=image)
            if serializer.is_valid():
                image = serializer.save()
                instance.image = image
            else:
                print(serializer.errors)
        instance.save()
        return instance


class SexualDifferentiationSerializer(serializers.ModelSerializer):
    youth = SDYouthSerializer(required=False)
    subadult = SDSubadultSerializer(required=False)
    female = SDFemaleSerializer(required=False)
    male = SDMaleSerializer(required=False)

    class Meta:
        model = SexualDifferentiation
        exclude = ('id',)

    def create(self, validated_data):
        youth = validated_data.pop('youth', None)
        if youth:
            serializer = SDYouthSerializer(data=youth)
            if serializer.is_valid():
                youth = serializer.save()
            else:
                print(serializer.errors)
        subadult = validated_data.pop('subadult', None)
        if subadult:
            serializer = SDSubadultSerializer(data=subadult)
            if serializer.is_valid():
                subadult = serializer.save()
            else:
                print(serializer.errors)
        female = validated_data.pop('female', None)
        if female:
            serializer = SDFemaleSerializer(data=female)
            if serializer.is_valid():
                female = serializer.save()
            else:
                print(serializer.errors)
        male = validated_data.pop('male', None)
        if male:
            serializer = SDMaleSerializer(data=male)
            if serializer.is_valid():
                male = serializer.save()
            else:
                print(serializer.errors)
        sexual_diff = SexualDifferentiation.objects.create(youth=youth, subadult=subadult, female=female, male=male)
        return sexual_diff

    def update(self, instance, validated_data):
        youth = validated_data.get('youth', None)
        if youth:
            serializer = SDYouthSerializer(instance.youth, data=youth)
            if serializer.is_valid():
                youth = serializer.save()
                instance.youth = youth
            else:
                print(serializer.errors)
        subadult = validated_data.get('subadult', None)
        if subadult:
            serializer = SDSubadultSerializer(instance.subadult, data=subadult)
            if serializer.is_valid():
                subadult = serializer.save()
                instance.subadult = subadult
            else:
                print(serializer.errors)
        female = validated_data.get('female', None)
        if female:
            serializer = SDFemaleSerializer(instance.female, data=female)
            if serializer.is_valid():
                female = serializer.save()
                instance.female = female
            else:
                print(serializer.errors)
        male = validated_data.get('male', None)
        if male:
            serializer = SDMaleSerializer(instance.male, data=male)
            if serializer.is_valid():
                male = serializer.save()
                instance.male = male
            else:
                print(serializer.errors)
        instance.save()
        return instance


class LengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Length
        exclude = ('id', 'bird')


class BirdSerializer(serializers.ModelSerializer):
    common_names = CommonNameBirdSerializer(required=False, many=True)
    # common_name_bird = CommonNameBirdSerializer(required=False, many=True)
    scientific_names = ScientificNameBirdSerializer(required=False, many=True)
    images = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)
    singing = AudioSerializer(many=True, required=False)
    heights = LengthSerializer(many=True, required=False)
    family = FamilySerializer(required=False)
    description = TextSerializer(required=False)
    identification = IdentificationSerializer(required=False)
    distribution = TextSerializer(required=False)
    habitat = HabitatSerializer(required=False)
    feeding = FeedingSerializer(required=False)
    reproduction = ReproductionSerializer(required=False)
    behavior = TextSerializer(required=False)
    taxonomy = TextSerializer(required=False)
    conservation = ConservationSerializer(required=False)
    sexual_differentiation = SexualDifferentiationSerializer(required=False)
    curiosities = TextSerializer(required=False)
    references = ReferenceSerializer(required=False, many=True)
    own_citation = ReferenceSerializer(required=False)

    class Meta:
        model = Bird
        fields = '__all__'

    def create(self, validated_data):
        family = validated_data.pop('family', None)
        if family:
            serializer = FamilySerializer(data=family)
            if serializer.is_valid():
                family = serializer.save()
            else:
                print(serializer.errors)
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
            distribution = Text.objects.create(**distribution)
        habitat = validated_data.pop('habitat', None)
        if habitat:
            serializer = HabitatSerializer(data=habitat)
            if serializer.is_valid():
                habitat = serializer.save()
            else:
                print(serializer.errors)
        feeding = validated_data.pop('feeding', None)
        if feeding:
            serializer = FeedingSerializer(data=feeding)
            if serializer.is_valid():
                feeding = serializer.save()
            else:
                print(serializer.errors)
        reproduction = validated_data.pop('reproduction', None)
        if reproduction:
            serializer = ReproductionSerializer(data=reproduction)
            if serializer.is_valid():
                reproduction = serializer.save()
            else:
                print(serializer.errors)
        behavior = validated_data.pop('behavior', None)
        if behavior:
            behavior = Text.objects.create(**behavior)
        taxonomy = validated_data.pop('taxonomy', None)
        if taxonomy:
            taxonomy = Text.objects.create(**taxonomy)
        conservation = validated_data.pop('conservation', None)
        if conservation:
            serializer = ConservationSerializer(data=conservation)
            if serializer.is_valid():
                conservation = serializer.save()
            else:
                print(serializer.errors)
        sexual_differentiation = validated_data.pop('sexual_differentiation', None)
        if sexual_differentiation:
            serializer = SexualDifferentiationSerializer(data=sexual_differentiation)
            if serializer.is_valid():
                sexual_differentiation = serializer.save()
            else:
                print(serializer.errors)
        curiosities = validated_data.pop('curiosities', None)
        if curiosities:
            curiosities = Text.objects.create(**curiosities)
        own_citation = validated_data.pop('own_citation', None)
        if own_citation:
            serializer = ReferenceSerializer(data=own_citation)
            if serializer.is_valid():
                own_citation = serializer.save()
            else:
                print(serializer.errors)

        common_names_data = validated_data.pop('common_names', [])
        scientific_names_data = validated_data.pop('scientific_names', [])
        images_data = validated_data.pop('images', [])
        videos_data = validated_data.pop('videos', [])
        singing_data = validated_data.pop('singing', [])
        heights_data = validated_data.pop('heights', [])
        bird = Bird.objects.create(family=family, description=description, identification=identification,
                                   distribution=distribution, habitat=habitat, feeding=feeding,
                                   reproduction=reproduction, behavior=behavior, taxonomy=taxonomy,
                                   conservation=conservation, sexual_differentiation=sexual_differentiation,
                                   curiosities=curiosities, own_citation=own_citation, **validated_data)

        common_names = []
        for common_name in common_names_data:
            main = 'main' in common_name and common_name.pop('main')
            serializer = TextSerializer(data=common_name['name'])
            if serializer.is_valid():
                name = serializer.save()
                c_n = CommonNameBird.objects.create(bird=bird, name=name,
                                                    main=main)
                c_n.save()
            else:
                print(serializer.errors)
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
            serializer = ImageSerializer(data=image)
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
        singing = []
        for sing in singing_data:
            serializer = AudioSerializer(data=sing)
            if serializer.is_valid():
                si = serializer.save()
                singing.append(si)
            else:
                print(serializer.errors)
        bird.singing.set(singing)
        heights = []
        for height in heights_data:
            serializer = LengthSerializer(data=height)
            if serializer.is_valid():
                he = serializer.save()
                heights.append(he)
            else:
                print(serializer.errors)
        bird.heights.set(heights)
        return bird

    def update(self, instance, validated_data):
        family = validated_data.pop('family', None)
        if family:
            serializer = FamilySerializer(instance.family, data=family)
            if serializer.is_valid():
                family = serializer.save()
                instance.family = family
            else:
                print(serializer.errors)
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
            serializer = TextSerializer(instance.distribution, data=distribution)
            if serializer.is_valid():
                distribution = serializer.save()
                instance.distribution = distribution
            else:
                print(serializer.errors)
        habitat = validated_data.pop('habitat', None)
        if habitat:
            serializer = HabitatSerializer(instance.habitat, data=habitat)
            if serializer.is_valid():
                habitat = serializer.save()
                instance.habitat = habitat
            else:
                print(serializer.errors)
        feeding = validated_data.pop('feeding', None)
        if feeding:
            serializer = FeedingSerializer(instance.feeding, data=feeding)
            if serializer.is_valid():
                feeding = serializer.save()
                instance.feeding = feeding
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
        behavior = validated_data.pop('behavior', None)
        if behavior:
            serializer = TextSerializer(instance.behavior, data=behavior)
            if serializer.is_valid():
                behavior = serializer.save()
                instance.behavior = behavior
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
            serializer = ConservationSerializer(instance.conservation, data=conservation)
            if serializer.is_valid():
                conservation = serializer.save()
                instance.conservation = conservation
            else:
                print(serializer.errors)
        sexual_differentiation = validated_data.pop('sexual_differentiation', None)
        if sexual_differentiation:
            serializer = SexualDifferentiationSerializer(instance.sexual_differentiation, data=conservation)
            if serializer.is_valid():
                sexual_differentiation = serializer.save()
                instance.sexual_differentiation = sexual_differentiation
            else:
                print(serializer.errors)
        curiosities = validated_data.pop('curiosities', None)
        if curiosities:
            serializer = TextSerializer(instance.curiosities, data=curiosities)
            if serializer.is_valid():
                curiosities = serializer.save()
                instance.curiosities = curiosities
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

        instance.common_names.all().delete()
        common_names_data = validated_data.pop('common_names', [])
        common_names = []
        for common_name in common_names_data:
            serializer = CommonNameBirdSerializer(data=common_name)
            if serializer.is_valid():
                si = serializer.save()
                common_names.append(si)
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
            serializer = ImageSerializer(data=image)
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
        instance.heights.all().delete()
        heights_data = validated_data.pop('heights', [])
        heights = []
        for height in heights_data:
            serializer = LengthSerializer(data=height)
            if serializer.is_valid():
                si = serializer.save()
                heights.append(si)
            else:
                print(serializer.errors)
        instance.heights.set(heights)
        instance.singing.all().delete()
        singing_data = validated_data.pop('singing', [])
        singing = []
        for sing in singing_data:
            serializer = AudioSerializer(data=sing)
            if serializer.is_valid():
                si = serializer.save()
                singing.append(si)
            else:
                print(serializer.errors)
        instance.singing.set(singing)
        instance.save()
        return instance
