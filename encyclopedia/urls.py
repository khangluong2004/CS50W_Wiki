from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("edit", views.edit, name = "edit"),
    path("search/result", views.search, name="search_result"),
    path("new", views.new, name="new"), 
    path("new/result", views.new_result, name="new_result"),
    path("random", views.random_entry, name = "random")
]
