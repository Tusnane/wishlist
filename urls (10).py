from django.urls import path

from . import views

urlpatterns = [
    path("", views.week, name="week"),
    path("add/", views.add, name="add"),
    path("toggle/<int:pk>/", views.toggle, name="toggle"),
    path("delete/<int:pk>/", views.delete, name="delete"),
]
