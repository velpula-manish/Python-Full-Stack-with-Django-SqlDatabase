from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'payment_method']
from django import forms
from .models import OrderItem, Order, MenuItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # No fields from Order itself (handled internally)
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'payment_method']
