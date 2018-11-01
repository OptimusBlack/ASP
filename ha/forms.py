from django import forms


class AddStockForm(forms.Form):
    product_name = forms.CharField(label='Product Name', max_length=200)
    product_price = forms.FloatField(label='Price')
