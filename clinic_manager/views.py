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
        o['id'] = product.id
        o['name'] = product.name
        o['price'] = product.price
        o['weight'] = product.weight_per_unit
        o['category'] = product.category
        o['description'] = product.description
        context['products'].append(o.copy())

    return render(request, 'clinic_manager/index.html', context=context)
