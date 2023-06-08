from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/" + "<str:name>", views.route_entry, name="route_entry"),
    path("new/", views.new, name="new"),
    path("edit/" + "<str:name>", views.edit, name="edit"),
    path("random/", views.random_entry, name="random_entry")
]
