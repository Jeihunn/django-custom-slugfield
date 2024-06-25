from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("test/<slug:slug>/", views.detail_view, name="detail_view"),
]