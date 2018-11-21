from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .functions import dispatch_order
from .models import DispatchQueue
from clinic_manager.models import Order
from ha.models import LocationData


def index(request):
    dispatch_queue = sorted(DispatchQueue.objects.all(), key=lambda x: x.queue_number)
    display_view = []
    if 'dispatch' not in request.session:
        request.session['dispatch'] = []
    for d in dispatch_queue:
        order_details = Order.objects.get(id=d.order_id)
        order_details.total_weight = round(order_details.total_weight, 2)
        display_view.append(order_details)

    print("DispatchQueue:", request.session['dispatch'])
    context = {
        'orders': display_view,
        'dispatch': request.session['dispatch']
    }
    return render(request, 'dispatcher/index.html', context=context)


def do_pop(request):
    dispatch_queue = sorted(DispatchQueue.objects.all(), key=lambda x: x.queue_number)
    if len(dispatch_queue) > 0:
        for d in dispatch_queue:
            d.queue_number = d.queue_number - 1
            d.save()

        order_to_dispatch = dispatch_queue[0]
        order_details = Order.objects.get(id=order_to_dispatch.order_id)
        request.session['dispatch'].append({'id': order_details.id, 'total_weight': order_details.total_weight})
        request.session.modified = True
        order_to_dispatch.delete()

    print("Session after process: ", request.session['dispatch'])
    return HttpResponse()


def dispatch(request):
    import csv
    orders_queued = request.session['dispatch']
    if len(orders_queued) > 0:
        for order in orders_queued:
            order_object = Order.objects.get(id=order['id'])
            order_object.order_status = 'Dispatched'
            order_object.time_dispatched = timezone.now()
            order_object.save()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="download.csv"'

        writer = csv.writer(response)
        for order in orders_queued:
            order_object = Order.objects.get(id=order['id'])
            location_data = LocationData.objects.get(name=order_object.order_clinic)
            writer.writerow([location_data.lat, location_data.lng, location_data.alt])
        location_data = LocationData.objects.get(name='Queen Mary Hospital Drone Port')
        writer.writerow([location_data.lat, location_data.lng, location_data.alt])
        writer.writerow([location_data.lat, location_data.lng, location_data.alt])
        request.session['dispatch'] = []
        return response
