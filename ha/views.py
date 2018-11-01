from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Stock


def add_to_database(data):
    """
    Adds the data argument to the database
    :param data: {'product_name': <String max = 200>, 'product_price': <Float>}
    :return: None
    """
    s = Stock()
    s.name = data['product_name']
    s.price = data['product_price']
    s.save()


def add_stock(request):
    """
    Add a product to the stock available for order
    :param request: request object
    :return: renders the form for input
    """
    from .forms import AddStockForm

    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            add_to_database(form.cleaned_data)
            return HttpResponseRedirect('/ha/addstock/')
    else:
        form = AddStockForm()

    return render(request, 'ha/addstock.html', {'form': form})
