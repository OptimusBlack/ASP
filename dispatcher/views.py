from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from ha.models import Item
from .models import DispatchQueue
from clinic_manager.models import Order, ClinicManager
from ha.models import LocationData
from ASP.global_functions import update_dispatch_queue, update_process_queue, route_plan
import json


def index(request):
    """
    Render the Dispatcher home page.
    :param request:
    :return: Render template
    """
    update_process_queue()
    update_dispatch_queue()

    dispatch_queue = DispatchQueue.objects.all().order_by('queue_number')

    if len(dispatch_queue) < 1:
        return render(request, 'dispatcher/index.html')

    if 'dispatch' not in request.session:
        request.session['dispatch'] = []

    orders = []
    weight = 0.0
    for order in dispatch_queue:
        order_details = Order.objects.get(id=order.order_id)
        order_details.total_weight = round(order_details.total_weight, 2)
        weight += order_details.total_weight

        if weight > 23.8:
            break

        order_details.content_details = []

        order_contents = json.loads(order_details.contents)['contents']
        for cont in order_contents:
            item = Item.objects.get(id=cont['product_id'])
            item.qty = cont['qty']
            order_details.content_details.append(item)

        orders.append(order_details)

    route_plan(orders)
    context = {
        'orders': orders
    }
    return render(request, 'dispatcher/index.html', context=context)


# def do_pop(request):
#     dispatch_queue = sorted(DispatchQueue.objects.all(), key=lambda x: x.queue_number)
#     if len(dispatch_queue) > 0:
#         for d in dispatch_queue:
#             d.queue_number = d.queue_number - 1
#             d.save()
#
#         order_to_dispatch = dispatch_queue[0]
#         order_details = Order.objects.get(id=order_to_dispatch.order_id)
#         request.session['dispatch'].append({'id': order_details.id, 'total_weight': order_details.total_weight})
#         request.session.modified = True
#         order_to_dispatch.delete()
#
#     print("Session after process: ", request.session['dispatch'])
#     return HttpResponse()


def dispatch(request):
    """
    Dispatch an order
    The function will:
        dispatch the order that can be contained in the next shipment
        send email to the clinic manager for each order within the shipment, as a notification.
    :param request:
    :return: CSV file as a response.
    """
    import csv
    orders_to_dispatch = DispatchQueue.objects.all().order_by('queue_number')

    if len(orders_to_dispatch) < 1:
        return HttpResponse("0")

    orders = []
    weight = 0

    for order in orders_to_dispatch:
        order_object = Order.objects.get(id=order.order_id)

        order_object.total_weight = round(order_object.total_weight, 2)
        weight += order_object.total_weight

        if weight > 23.8:
            break

        orders.append(order_object)

        order_object.order_status = 'Dispatched'
        order_object.time_dispatched = timezone.now()
        order_object.save()

        clinic_manager_email = (ClinicManager.objects.get(clinic_name= order_object.order_clinic)).user.email

        send_mail(
            'Order Dispatched',
            'Your order with order number: ' + str(order_object.id) + ' has been dispatched from the hospital.',
            'ha@example.com',
            [clinic_manager_email]
        )

    csv_route = route_plan(orders)

    update_dispatch_queue()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="download.csv"'

    writer = csv.writer(response)
    for destination in csv_route:
        location_data = LocationData.objects.get(name=destination)
        writer.writerow([location_data.lat, location_data.lng, location_data.alt])

    # for order in orders:
    #     location_data = LocationData.objects.get(name=order.order_clinic)
    #     writer.writerow([location_data.lat, location_data.lng, location_data.alt])

    # location_data = LocationData.objects.get(name='Queen Mary Hospital Drone Port')
    # writer.writerow([location_data.lat, location_data.lng, location_data.alt])
    request.session['dispatch'] = []
    return response
