from django.shortcuts import render
from .models import Customer,Place,OrderedItem,MenuCategory,MenuItem,Reservation,Waiter
from django.http import HttpResponse

def index(request):
    context = {
        "render_string": "Hello,world"
    }
    return render(request, "restic/index.html", context)

def place_list(request):
    place = Place.objects.all()
    context = {
        "place_list": place,
    }
    return render(request,"restic/place_list.html",context)

def menu_category(request):
    category = MenuCategory.objects.all()
    context = {
        "menu_category": category
    }
    return render(request,"restic/menu_category.html",context)