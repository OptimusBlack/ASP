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
from warehouse.models import ProcessQueue
from .functions import place_order_for_user
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
    my_order_list = []
    for list_item in order_list:
        order_contents = json.loads(list_item.contents)
        contents_list = []
        for content in order_contents['contents']:
            item_in_content = Item.objects.get(id=int(content['product_id'])).name
            item_quantity = content['qty']
            contents_list.append({'name': item_in_content, 'qty': item_quantity})

        print(contents_list)
        my_order_list.append({
            'id': list_item.id,
            'total_weight': list_item.total_weight,
            'contents': contents_list,
            'order_status': list_item.order_status
        })

    context = {
        'orders': my_order_list
    }

    print(context)

    return render(request, 'clinic_manager/orders.html', context=context)


@csrf_exempt
def notify_delivery(request):
    if request.method == 'POST':
        req_obj = json.loads(request.body.decode('utf-8'))
        order_id = req_obj['order_id']
        order_object = Order.objects.get(id=order_id)
        order_object.time_delivered = timezone.now()
        order_object.order_status = "Delivered"
        order_object.save()

    return HttpResponse()


@csrf_exempt
def cancel_order(request):
    if request.method == 'POST':
        req_obj = json.loads(request.body.decode('utf-8'))
        order_id = req_obj['order_id']
        order_object = Order.objects.get(id=order_id)

        # Delete only if the order is queued for processing
        if order_object.order_status == "Queued for Processing":
            try:
                if ProcessQueue.objects.get(order_id=order_id):
                    # Delete if in process queue
                    process_queue_object = ProcessQueue.objects.get(order_id=order_id)
                    process_queue_object.delete()
                    current_process_queue = sorted(ProcessQueue.objects.all(), key=lambda x: x.queue_no)
                    i = 1
                    for contents in current_process_queue:
                        contents.queue_no = i
                        contents.save()
                        i += 1

            except ProcessQueue.DoesNotExist:
                pass

            order_object.delete()

    return HttpResponse()
