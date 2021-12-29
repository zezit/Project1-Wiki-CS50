from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("save_page/", views.save_page, name="save_page"),
    path("<str:title>/editPage", views.edit_page, name="edit_page"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random_page", views.random_page, name="random_page"),
]
