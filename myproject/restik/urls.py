from django.urls import path
from unicodedata import category

from .views import index, place_list, menu_category, category_detail, order_detail, book_table, order_list

urlpatterns = [
    path("", index, name ="index"),
    path("place-list", place_list, name ="place-list"),
    path("menu-category", menu_category, name ="menu-category"),
    path('menu/<int:category_id>/', category_detail, name='category_detail'),
    path('book-table/', book_table, name='book_table'),
    path('orders/', order_list, name = 'order_list'),
    path('orders/<int:reservation_id>/', order_detail, name='order_detail'),
]


