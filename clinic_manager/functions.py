import json
from .models import Order
from .models import ClinicManager
from ha.models import Item


def place_order_for_user(cart):
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
    new_order.priority_level = 0
    new_order.create_order()
