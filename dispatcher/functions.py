from .models import DispatchQueue
from clinic_manager.models import Order


def dispatch_order(request):
    dispatch_queue = sorted(DispatchQueue.objects.all(), key=lambda x: x.queue_number)
    if len(dispatch_queue) > 0:
        for d in dispatch_queue:
            d.queue_number = d.queue_number - 1
            d.save()

        order_to_dispatch = dispatch_queue[0]
        order_to_dispatch.delete()
        order_details = Order.objects.get(id=order_to_dispatch.order_id)
        request.session['dispatch'].append({'id': order_details.id, 'total_weight': order_details.total_weight})
        request.session.modified = True
        return request

