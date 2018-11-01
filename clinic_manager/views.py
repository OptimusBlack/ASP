"""
    @author: Utkarsh Goel <utkarsh867>

    Views for the Clinic Manager
    Handles all the requests that will be made by the clinic manager to the application

"""

from django.shortcuts import render
from ha.models import Stock


def index(request):
    stock_available = Stock.objects.all()
    context = {
        'products': []
    }
    o = {
        'name': "",
        'price': ""
    }

    for product in stock_available:
        o['name'] = product.name
        o['price'] = product.price
        context['products'].append(o.copy())

    print(context)
    return render(request, 'clinic_manager/index.html', context=context)
