from django import forms


class DeliveryNotification(forms.Form):
    order_id = forms.IntegerField()

