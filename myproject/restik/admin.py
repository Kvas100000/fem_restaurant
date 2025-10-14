from django.contrib import admin

from .models import (Customer,Place,OrderedItem,MenuCategory,MenuItem,Reservation,Waiter)

admin.site.register(Customer)
admin.site.register(Waiter)
admin.site.register(Place)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(Reservation)
admin.site.register(OrderedItem)
