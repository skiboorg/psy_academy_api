from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"faculties", FacultyViewSet)
router.register(r"education-formats", EducationFormatViewSet)
router.register(r"programs", EducationProgramViewSet)
router.register(r"news", NewsViewSet)
router.register(r"lecture", LectureViewSet)
router.register(r"lecture-formats", LectureFormatViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('news_tags', GetTags.as_view()),
]