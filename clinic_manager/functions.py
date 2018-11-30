import json
from .models import Order
from ha.models import Item
from warehouse.models import ProcessQueue
from ASP.global_functions import update_process_queue

def place_order_for_user(cart, clinic, priority=2):
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
    new_order.priority_level = int(priority)
    new_order.create_order(clinic)

    update_process_queue()

    return True
