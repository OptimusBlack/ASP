from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from .models import ProcessQueue, WarehousePersonnel
from ha.models import Item
from dispatcher.models import DispatchQueue
from clinic_manager.models import Order
from reportlab.pdfgen import canvas
import io
import json
from ASP.global_functions import update_process_queue, update_dispatch_queue

def index(request):
    WarehousePersonnel.objects.get(user=request.user)
    update_process_queue()
    update_dispatch_queue()
    process_queue_top = ProcessQueue.objects.filter(queue_no = 0)

    order_details = None
    if (len(process_queue_top) >= 1):
        if 'process' not in request.session:
            request.session['process'] = []

        order_details = Order.objects.get(id=process_queue_top[0].order_id)
        order_details.total_weight = round(order_details.total_weight, 2)
        order_details.content_details = []

        order_contents = json.loads(order_details.contents)['contents']
        for cont in order_contents:
            item = Item.objects.get(id=cont['product_id'])
            item.qty = cont['qty']
            order_details.content_details.append(item)


    order_in_process = Order.objects.filter(order_status='Processing by Warehouse')
    print(order_in_process)
    order_warehouse = None

    if (len(order_in_process) > 0):
        for order in order_in_process:
            order.content_details = []
            order_contents = json.loads(order.contents)['contents']
            for cont in order_contents:
                item = Item.objects.get(id=cont['product_id'])
                item.qty = cont['qty']
                order.content_details.append(item)
        order_warehouse = order_in_process[0]


    context = {
        'order': order_details,
        'warehouse': order_warehouse
    }
    return render(request, 'warehouse/index.html', context=context)


def do_pop(request):
    WarehousePersonnel.objects.get(user=request.user)
    processing_orders = Order.objects.filter(order_status='Processing by Warehouse')
    if len(processing_orders) > 0:
        return HttpResponse(json.dumps({'msg': 1}))

    process_queue_top = ProcessQueue.objects.get(queue_no=0)
    order = Order.objects.get(id=process_queue_top.order_id)

    order.order_status = 'Processing by Warehouse'
    order.save()

    request.session['process'].append({'id': order.id, 'total_weight': order.total_weight})
    request.session.modified = True

    update_process_queue()

    print(request.session['process'])
    return HttpResponse(json.dumps({'msg': 0}))


def process(request):
    WarehousePersonnel.objects.get(user=request.user)
    order_object = Order.objects.filter(order_status='Processing by Warehouse')
    if (len(order_object) < 1):
        return HttpResponse("0")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, 'AS-P')
    i = 650

    for order in order_object:
        p.drawString(100, i, "Order Number: " + str(order.id))
        contents = order.contents
        contents = json.loads(contents)
        for content in contents['contents']:
            item_object = Item.objects.get(id=content['product_id'])
            p.drawString(100, i-50, str(item_object.name) + '; Quantity: ' + str(content['qty']))
            i = i - 50

        p.drawString(100, i - 50, str(order.order_clinic))
        order.order_status = 'Queued for Dispatch'
        order.save()

    print('Queued for Dispatch...')
    update_dispatch_queue()

    request.session['process'] = []
    request.session.modified = True

    p.showPage()
    p.save()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "shipping_label.pdf"'
    response.write(buffer.getvalue())
    return response
