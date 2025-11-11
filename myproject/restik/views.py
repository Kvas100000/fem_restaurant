from django.shortcuts import render, get_object_or_404,redirect
from .models import Customer,Place,OrderedItem,MenuCategory,MenuItem,Reservation,Waiter
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime


def index(request):
    context = {
        "render_string": "Hello,world"
    }
    return render(request, "restik/index.html", context)

def place_list(request):
    place = Place.objects.all()
    context = {
        "place_list": place,
    }
    return render(request,"restik/place_list.html",context)

def menu_category(request):
    category = MenuCategory.objects.all()
    context = {
        "menu_category": category
    }
    return render(request,"restik/menu_category.html",context)


def category_detail(request, category_id):
    category = get_object_or_404(MenuCategory, pk=category_id)
    menu_items = category.items.all().order_by('name')

    context = {
        'category': category,
        'menu_items': menu_items,
    }
    return render(request, 'restik/category_detail.html', context)

@login_required
def book_table(request):
    all_menus = MenuItem.objects.all()
    available_places = Place.objects.all()

    context = {
        'menu_items': all_menus,
        'available_places': available_places,
    }

    if request.method == "POST":
        menu_ids = request.POST.getlist('menu-name')
        start_time_raw = request.POST.get('start-time')
        end_time_raw = request.POST.get('end-time')
        place_id = request.POST.get('place-id')

        if not menu_ids or not start_time_raw or not end_time_raw or not place_id:
            context['error'] = 'Пожалуйста заполните все поля'
            return render(request, 'restik/booking_form.html', context=context)

        try:
            start_dt = datetime.fromisoformat(start_time_raw)
            end_dt = datetime.fromisoformat(end_time_raw)
            if timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt)
            if timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt)
        except Exception:
            context['error'] = 'Неверный формат даты'
            return render(request, 'restik/booking_form.html', context=context)

        if end_dt <= start_dt:
            context['error'] = 'Время окончания должно быть позже начала'
            return render(request, 'restik/booking_form.html', context=context)

        place = get_object_or_404(Place, pk=place_id)
        overlapping = Reservation.objects.filter(
            place=place,
            start_time__lt=end_dt,
            end_time__gt=start_dt
        )
        if overlapping.exists():
            context['error'] = f"Столик №{place.table_number} занят в выбранное время"
            return render(request, 'restik/booking_form.html', context=context)

        customer, _ = Customer.objects.get_or_create(user=request.user, defaults={'name': request.user.get_full_name() or 'Anonim'})

        reservation = Reservation.objects.create(
            customer=customer,
            place=place,
            start_time=start_dt,
            end_time=end_dt,
            notes=""
        )

        for menu_id in menu_ids:
            try:
                menu_item = MenuItem.objects.get(id=menu_id)
                OrderedItem.objects.create(reservation=reservation, menu_item=menu_item, quantity=1)
            except MenuItem.DoesNotExist:
                continue

        return redirect('order_detail', reservation_id=reservation.id)

    return render(request, 'restik/booking_form.html', context=context)





@login_required
def order_list(request):
    now = timezone.now()
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        bookings = Reservation.objects.none()
    else:
        bookings = Reservation.objects.filter(
            customer=customer,
            end_time__gt=now
        ).order_by('start_time')
    return render(request, 'restik/order_list.html', {'bookings': bookings})



@login_required
def order_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.customer.user != request.user:
        raise Http404
    ordered_items = reservation.ordered_items.select_related('menu_item').all()
    return render(request, 'restik/order-detail.html', {'reservation': reservation, 'ordered_items': ordered_items})






