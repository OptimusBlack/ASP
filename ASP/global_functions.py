from clinic_manager.models import Order
from warehouse.models import ProcessQueue
from dispatcher.models import DispatchQueue

def update_process_queue():
    orders = Order.objects.filter(order_status='Queued for Processing').order_by('priority_level', 'date_ordered')
    ProcessQueue.objects.all().delete()

    queue_no =0

    for order in orders:
        p = ProcessQueue()
        p.order_id = order.id
        p.queue_no = queue_no
        queue_no += 1
        p.save()

    print('Process queue updated')

def update_dispatch_queue():
    orders = Order.objects.filter(order_status='Queued for Dispatch').order_by('priority_level', 'date_ordered')
    DispatchQueue.objects.all().delete()

    queue_no = 0

    for order in orders:
        q = DispatchQueue()
        q.order_id = order.id
        q.queue_number = queue_no
        queue_no += 1
        q.save()

    print('Dispatch queue updated')