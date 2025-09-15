from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# ==========================
# Inlines для Program
# ==========================
class ProgramAboutItemInline(admin.TabularInline):
    model = ProgramAboutItem
    extra = 0





class ProgramModuleInline(admin.StackedInline):
    model = ProgramModule
    extra = 0



@admin.register(EducationProgram)
class EducationProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "faculty", "format", "show_on_main", "order")
    list_filter = ("faculty", "format", "show_on_main")
    search_fields = ("id", "name", "faculty__name", "format__name")
    inlines = [ProgramAboutItemInline, ProgramModuleInline]


# ==========================
# Faculty
# ==========================
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")


# ==========================
# EducationFormat
# ==========================
@admin.register(EducationFormat)
class EducationFormatAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")

@admin.register(EducationProgramTag)
class EducationProgramTagAdmin(admin.ModelAdmin):
    list_display = ("label",)

# ==========================
# LectureFormat
# ==========================
@admin.register(LectureFormat)
class LectureFormatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color")
    search_fields = ("id", "name", "color")









class LectureAboutItemInline(admin.TabularInline):
    model = LectureAboutItem
    extra = 0

class LectureForItemInline(admin.TabularInline):
    model = LectureForItem
    extra = 0


class LectureModuleInline(admin.StackedInline):
    model = LectureModule
    extra = 0


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("id", "name",  "format", "order")
    list_filter = ("format", )
    search_fields = ("id", "name", )
    inlines = [LectureAboutItemInline,LectureForItemInline,LectureModuleInline]

@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("author",'text1',)


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name",'created_at','creator')
    list_filter = ("tags",)
    search_fields = ("id", "name","creator__full_name")