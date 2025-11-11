from django.db import models
from django.conf import settings

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, default='Anonim')
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username if self.user else self.name


class Waiter(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Place(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.table_number}"

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category =models.ForeignKey(MenuCategory,on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    waiter = models.ForeignKey(Waiter, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.customer} — {self.start_time}"




class OrderedItem(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='ordered_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"




