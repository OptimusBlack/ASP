from django.shortcuts import render
from .models import ProcessQueue
from clinic_manager.models import Order


def index(request):
    process_queue = sorted(ProcessQueue.objects.all(), key=lambda x: x.queue_no)
    display_view = []
    if 'process' not in request.session:
        request.session['process'] = []
    for d in process_queue:
        order_details = Order.objects.get(id=d.order_id)
        order_details.total_weight = round(order_details.total_weight, 2)
        display_view.append(order_details)

    print("DispatchQueue:", request.session['process'])
    context = {
        'orders': display_view,
        'warehouse': request.session['process']
    }
    return render(request, 'warehouse/index.html', context=context)
