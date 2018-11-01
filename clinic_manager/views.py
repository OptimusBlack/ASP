"""
    @author: Utkarsh Goel <utkarsh867>

    Views for the Clinic Manager
    Handles all the requests that will be made by the clinic manager to the application

"""

from django.shortcuts import render
from ha.models import Stock


def index(request):
    """
    Render the home for the Clinic Manager
    :param request: Request object
    :return: renders the homepage for the clinic manager
    """
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

    return render(request, 'clinic_manager/index.html', context=context)
