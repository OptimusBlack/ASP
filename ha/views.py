from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Stock


def add_to_database(data):
    """
        The data is in the form of a JSON object:
            {'product_name': 'Name', 'product_price': 12.0}
    """
    s = Stock()
    s.name = data['product_name']
    s.price = data['product_price']
    s.save()


def add_stock(request):
    from .forms import AddStockForm

    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            add_to_database(form.cleaned_data)
            return HttpResponseRedirect('/ha/addstock/')
    else:
        form = AddStockForm()

    return render(request, 'ha/addstock.html', {'form': form})
