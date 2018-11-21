from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from .models import ProcessQueue
from ha.models import Item
from dispatcher.models import DispatchQueue
from clinic_manager.models import Order
from reportlab.pdfgen import canvas
import io
import json

def index(request):
    process_queue = sorted(ProcessQueue.objects.all(), key=lambda x: x.queue_no)
    display_view = []
    if 'process' not in request.session:
        request.session['process'] = []
    for d in process_queue:
        order_details = Order.objects.get(id=d.order_id)
        order_details.total_weight = round(order_details.total_weight, 2)
        display_view.append(order_details)

    print(request.session['process'])
    context = {
        'orders': display_view,
        'warehouse': request.session['process']
    }
    return render(request, 'warehouse/index.html', context=context)


def do_pop(request):
    process_queue = sorted(ProcessQueue.objects.all(), key=lambda x: x.queue_no)
    if len(process_queue) > 0:
        for d in process_queue:
            d.queue_no = d.queue_no - 1
            order_object = Order.objects.get(id=d.order_id)
            order_object.order_status = 'Processing by Warehouse'
            order_object.save()
            d.save()

        order_to_process = process_queue[0]
        order_details = Order.objects.get(id=order_to_process.order_id)
        request.session['process'].append({'id': order_details.id, 'total_weight': order_details.total_weight})
        request.session.modified = True
        order_to_process.delete()
        print(request.session['process'])
    return HttpResponse()


def process(request):
    orders_queued = request.session['process']
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, 'AS-P')
    i = 650
    if len(orders_queued) > 0:
        for order in orders_queued:
            order_object = Order.objects.get(id=order['id'])
            p.drawString(100, i, "Order Number: " + str(order['id']))
            contents = order_object.contents
            contents = json.loads(contents)
            for content in contents['contents']:
                item_object = Item.objects.get(id=content['product_id'])
                p.drawString(100, i-50, str(item_object.name) + '; Quantity: ' + content['qty'])
                i = i - 50

            p.drawString(100, i - 50, str(order_object.order_clinic))
            order_object.order_status = 'Queued for Dispatch'
            order_object.save()

            # Add to Dispatch Queue
            current_dispatch_queue = sorted(DispatchQueue.objects.all(), key=lambda x: x.queue_number)
            if len(current_dispatch_queue) == 0:
                new_queue_no = 1
            else:
                last_in_queue = current_dispatch_queue[len(current_dispatch_queue) - 1]
                new_queue_no = last_in_queue.queue_number + 1

            d = DispatchQueue()
            d.queue_number = new_queue_no
            d.order_id = order['id']
            d.save()
        request.session['process'] = []

    p.showPage()
    p.save()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "shipping_label.pdf"'
    response.write(buffer.getvalue())
    return response
