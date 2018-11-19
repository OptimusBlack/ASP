import json
from .models import Order
from ha.models import Item
from warehouse.models import ProcessQueue


def place_order_for_user(cart, clinic, priority='Low'):
    permissible_weight = 23.5
    total_weight = 0
    new_order = Order()
    for item in cart:
        i = Item.objects.get(id = item['product_id'])
        qty = int(item['qty'])
        total_weight += i.weight_per_unit * qty
        print(json.loads(new_order.contents))
        content_list = json.loads(new_order.contents)['contents']
        content_list.append(item)
        new_order.contents = json.dumps({'contents': content_list})

    new_order.total_weight = total_weight

    if total_weight > permissible_weight:
        return False
    new_order.priority_level = priority
    new_order.create_order(clinic)

    p = ProcessQueue()
    p.order_id = new_order.id
    current_process_queue = sorted(ProcessQueue.objects.all(), key=lambda x: x.queue_number)
    if len(current_process_queue) == 0:
        new_queue_no = 1
    else:
        last_in_queue = current_process_queue[len(current_process_queue) - 1]
        new_queue_no = last_in_queue.queue_number + 1

    p.queue_no = new_queue_no
    p.save()

    return True
