"""
    @author: Utkarsh Goel <utkarsh867>

    Views for the Clinic Manager
    Handles all the requests that will be made by the clinic manager to the application

"""

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ha.models import Item
from .functions import place_order_for_user
import json


def index(request):
    """
    Render the home for the Clinic Manager
    :param request: Request object
    :return: renders the homepage for the clinic manager
    """
    request.session['cart'] = []
    stock_available = Item.objects.all()
    context = {
        'products': []
    }
    o = {
        'name': "",
        'price': ""
    }

    for product in stock_available:
        o['id'] = product.id
        o['name'] = product.name
        o['price'] = product.price
        o['weight'] = product.weight_per_unit
        o['category'] = product.category
        o['description'] = product.description
        context['products'].append(o.copy())

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


def place_order(request):
    if len(request.session['cart']) > 0:
        place_order_for_user(request.session['cart'])
        request.session['cart'] = []
        request.session.modified = True
    return HttpResponse()
