from rest_framework import serializers
from .models import *


class LectureTariffItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureTariffItem
        fields = "__all__"


class LectureTariffSerializer(serializers.ModelSerializer):
    tariff_items = LectureTariffItemsSerializer(many=True, read_only=True)
    class Meta:
        model = LectureTariff
        fields = "__all__"


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class EducationFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationFormat
        fields = ['name']


class ProgramAboutItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramAboutItem
        fields = "__all__"




class ProgramModuleSerializer(serializers.ModelSerializer):
    # items = ProgramModuleItemSerializer(many=True, read_only=True)

    class Meta:
        model = ProgramModule
        fields = "__all__"


class ProgramForItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramForItem
        fields = "__all__"

class ProgramFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramFeature
        fields = "__all__"


class EducationProgramTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationProgramTag
        fields = ['label']



class EducationProgramSerializer(serializers.ModelSerializer):
    tags = EducationProgramTagSerializer(many=True, read_only=True)
    about_items = ProgramAboutItemSerializer(many=True, read_only=True)
    modules = ProgramModuleSerializer(many=True, read_only=True)
    format = EducationFormatSerializer(read_only=True)
    p_for_items = ProgramForItemSerializer(many=True, read_only=True)
    p_features = ProgramFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = EducationProgram
        fields = "__all__"

class EducationProgramShortSerializer(serializers.ModelSerializer):
    tags = EducationProgramTagSerializer(many=True, read_only=True)
    format = EducationFormatSerializer(read_only=True)
    #faculty = FacultySerializer(read_only=True)
    class Meta:
        model = EducationProgram
        fields = [
            'tags',
            #'faculty',
            'name',
            'slug',
            'short_description',
            'duration',
            'price',
            'format'
        ]


class LectureFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureFormat
        fields = "__all__"


class LectureAboutItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureAboutItem
        fields = "__all__"

class LectureForItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureForItem
        fields = "__all__"


class LectureModuleSerializer(serializers.ModelSerializer):
    # items = ProgramModuleItemSerializer(many=True, read_only=True)

    class Meta:
        model = LectureModule
        fields = "__all__"

class PartnerSerializer(serializers.ModelSerializer):
    # items = ProgramModuleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = "__all__"

class LectureSerializer(serializers.ModelSerializer):
    tariff = LectureTariffSerializer(read_only=True)

    for_items = LectureForItemSerializer(many=True, read_only=True)
    about_items = LectureAboutItemSerializer(many=True, read_only=True)
    lecture_modules = LectureModuleSerializer(many=True, read_only=True)
    format = LectureFormatSerializer(read_only=True)
    class Meta:
        model = Lecture
        fields = "__all__"

    def to_representation(self, instance):
        from user.serializers import UserStaffSerializer  # импорт здесь
        self.fields['teachers'] = UserStaffSerializer(many=True,read_only=True)
        return super().to_representation(instance)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class LectionFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectionForm
        fields = '__all__'

class QuestionFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionForm
        fields = '__all__'

class NewsItemShortSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,read_only=True)
    class Meta:
        model = NewsItem
        exclude = ['content']


class NewsItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,read_only=True)
    class Meta:
        model = NewsItem
        fields = '__all__'
