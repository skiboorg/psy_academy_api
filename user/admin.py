from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import UserCreationForm, UserChangeForm

class UserBiographyItemInline(admin.TabularInline):
    model = UserBiographyItem
    extra = 1


class UserFileLinkInline(admin.TabularInline):
    model = UserFileLink
    extra = 1



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "id",
        "full_name",
        "phone",
        "email",
        "is_teacher",
        "is_staff",
        "is_manager",
        "is_active",
        "is_superuser",
    )
    search_fields = ("id", "full_name", "phone", "email")
    ordering = ("id",)
    list_filter = (
        "is_teacher",
        "is_staff",
        "is_manager",
        "is_active",
        "is_superuser",
    )
    inlines = [UserBiographyItemInline, UserFileLinkInline]
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Персональная информация", {
            "fields": (
                "full_name",
                "email",
                "avatar",
                "photo",
                "birth_date",
                "position",
                "short_description",
                "quality",
                "tags",
                "work_time"
            )
        }),
        ("Роли", {
            "fields": (
                "is_teacher",
                "is_staff",
                "is_manager",
            )
        }),
        ("Права", {
            "fields": (
                "is_active",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "full_name",
                "phone",
                "email",
                "password1",
                "password2",
                "is_teacher",
                "is_staff",
                "is_manager",
                "is_active",
                "is_superuser",
            ),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserTag)
