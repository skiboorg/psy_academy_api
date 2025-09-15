from rest_framework import viewsets
from rest_framework import generics
from .models import *
import random
from django.db.models import Max
from .serializers import *


class FacultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    lookup_field = 'slug'


class EducationFormatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EducationFormat.objects.all()
    serializer_class = EducationFormatSerializer


class LectureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    lookup_field = "slug"

class GetTags(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = NewsTag.objects.all()

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsItem.objects.all()
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        show_on_main = self.request.query_params.get("show_on_main")
        tag = self.request.query_params.get("tag")
        random_count = self.request.query_params.get("random")
        if show_on_main:
            queryset = queryset.filter(show_on_main=True)
        if tag:
            queryset = queryset.filter(tags_in=[tag])
        if random_count:
            queryset = queryset.order_by("?")[:int(random_count)]
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NewsItemSerializer
        return NewsItemShortSerializer


class EducationProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EducationProgram.objects.all()
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        show_on_main = self.request.query_params.get("show_on_main")
        if show_on_main:
            queryset = queryset.filter(show_on_main=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EducationProgramSerializer
        return EducationProgramShortSerializer

class LectureFormatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LectureFormat.objects.all()
    serializer_class = LectureFormatSerializer

