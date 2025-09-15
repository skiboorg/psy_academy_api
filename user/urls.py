from django.urls import path,include
from . import views

urlpatterns = [
    path('me', views.GetUser.as_view()),
    path('update', views.UpdateUser.as_view()),
    path('staff', views.GetStaff.as_view()),
    path('staff/<slug>', views.GetStaffBySlug.as_view()),
]
