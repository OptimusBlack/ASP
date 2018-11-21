"""
    @author: Utkarsh Goel <utkarsh867>

    Views for the Clinic Manager
    Handles all the requests that will be made by the clinic manager to the application

"""

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from ha.models import Item
from .models import ClinicManager
from .models import Order
from .functions import place_order_for_user
from .forms import DeliveryNotification
import json


def index(request):
    """
    Render the home for the Clinic Manager
    :param request: Request object
    :return: renders the homepage for the clinic manager
    """

    current_user = ClinicManager.objects.get(user=request.user)
    request.session['cart'] = []
    request.session['clinic'] = current_user.clinic_name

    stock_available = Item.objects.all()
    context = {
        'products': [],
        'cart': []
    }
    o = {
        'name': "",
        'price': ""
    }

    for product in stock_available:
        o['id'] = product.id
        o['name'] = product.name
        o['weight'] = product.weight_per_unit
        o['category'] = product.category
        o['description'] = product.description
        o['image'] = product.image

        context['products'].append(o.copy())
        context['cart'] = request.session['cart']

    return render(request, 'clinic_manager/index.html', context=context)


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        """
        Using sessions to manage the cart
        """
        request.session['cart'].append(req)
        request.session.modified = True
        print(request.session['cart'])
        return HttpResponse("Done")


@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        if len(request.session['cart']) > 0:
            if place_order_for_user(request.session['cart'], request.session['clinic'], req['priority']):

                request.session['cart'] = []
                request.session.modified = True
                return HttpResponse(json.dumps({'status': 'success'}))
            else:
                request.session['cart'] = []
                return HttpResponse(json.dumps({'status': 'overweight'}))
        else:
            return HttpResponse(json.dumps({'status': 'emptycart'}))
    else:
        return HttpResponse()


def ordered_list(request):
    current_user = ClinicManager.objects.get(user=request.user)
    order_list = Order.objects.filter(order_clinic=current_user.clinic_name)

    context = {
        'orders': order_list
    }

    print(context)

    return render(request, 'clinic_manager/orders.html', context=context)


def notify_delivery(request):
    if request.method == 'POST':
        form = DeliveryNotification(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            order_object = Order.objects.get(id=order_id)
            order_object.time_delivered = timezone.now()
            order_object.order_status = "Delivered"
            order_object.save()
    else:
        form = DeliveryNotification()

    return render(request, 'clinic_manager/register.html', {'form': form})
