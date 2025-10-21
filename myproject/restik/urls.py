from django.urls import path
from .views import index, place_list, menu_category

urlpatterns = [
    path("", index, name ="index"),
    path("place-list", place_list, name ="place-list"),
    path("menu-category", menu_category, name ="menu-category"),
]