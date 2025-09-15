from rest_framework import serializers
from .models import *


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


class EducationProgramTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationProgramTag
        fields = ['label']

class EducationProgramSerializer(serializers.ModelSerializer):
    tags = EducationProgramTagSerializer(many=True, read_only=True)
    about_items = ProgramAboutItemSerializer(many=True, read_only=True)
    modules = ProgramModuleSerializer(many=True, read_only=True)
    format = EducationFormatSerializer(read_only=True)
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

class LectureSerializer(serializers.ModelSerializer):


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
