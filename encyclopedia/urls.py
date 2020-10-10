from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/searchresult", views.searchResults, name="searchResults"),
    path("wiki/new_page", views.new, name="newPage"),
    path("wiki/random", views.RandomPage, name="random"),
    path("wiki/<str:entry>", views.showEntry, name="showEntry"),
    path("wiki/<str:entry>/edit", views.edit, name="editPage")
]
