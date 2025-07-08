# views.py (Cleaned & Corrected Version)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.db import transaction

from .models import MenuItem, Order, OrderItem, Bill
from .forms import OrderForm
from decimal import Decimal


# ---------------------------
# User Login
# ---------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'cafe_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'cafe_app/login.html')

# ---------------------------
# Dashboard
# ---------------------------
@login_required
# cafe_app/views.py

def dashboard_view(request):
    # Summary statistics
    total_orders = Order.objects.count()
    total_sales = sum(order.total_price for order in Order.objects.all())
    total_items = MenuItem.objects.count()
    low_stock_items = MenuItem.objects.filter(stock__lt=5)

    # Lists for tables
    menu_items = MenuItem.objects.all()
    orders = Order.objects.order_by('-created_at')[:5]
    bills = Bill.objects.order_by('-generated_at')[:5]

    context = {
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_items': total_items,
        'low_stock_items': low_stock_items,
        'menu_items': menu_items,
        'orders': orders,
        'bills': bills
    }

    return render(request, 'cafe_app/dashboard.html', context)

# ---------------------------
# Menu
# ---------------------------
@login_required
def menu_view(request):
    items = MenuItem.objects.all()
    return render(request, 'cafe_app/menu.html', {'items': items})

# ---------------------------
# Inventory
# ---------------------------
@login_required
def inventory_view(request):
    items = MenuItem.objects.all()
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids')
        quantities = request.POST.getlist('quantities')
        for i in range(len(item_ids)):
            try:
                item = MenuItem.objects.get(id=item_ids[i])
                added_qty = int(quantities[i])
                item.stock += added_qty
                item.save()
            except:
                continue
        return redirect('inventory')
    return render(request, 'cafe_app/inventory.html', {'items': items})

# ---------------------------
# Place Order
# ---------------------------
@login_required

def place_order_view(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        payment_method = request.POST['payment_method']
        order = Order.objects.create(customer_name=customer_name, payment_method=payment_method)

        total = Decimal('0.00')
        for item_id, qty in request.POST.items():
            if item_id.startswith('item_') and int(qty) > 0:
                menu_item_id = int(item_id.split('_')[1])
                menu_item = MenuItem.objects.get(id=menu_item_id)
                quantity = int(qty)

                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
                total += menu_item.price * quantity

        order.total_price = total
        order.save()

        return redirect('order_success', order_id=order.id)


# ---------------------------
# Order Success
# ---------------------------
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cafe_app/order_success.html', {'order': order})

# ---------------------------
# Generate Bill
# ---------------------------
@login_required

def generate_bill(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Check if bill already exists for this order
    bill, created = Bill.objects.get_or_create(order=order, defaults={
        'total_amount': order.total_price,
        'payment_method': 'UPI',  # or 'Cash' based on logic
    })

    return render(request, 'cafe_app/generate_bill.html', {'bill': bill})


# ---------------------------
# Final Bill View
# ---------------------------

# ---------------------------
# UPI Payment
# ---------------------------
@login_required
def upi_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # ✅ Set your UPI ID here (you can change this)
    upi_id = "cafemanager@upi"

    # ✅ Image path for QR code (make sure this image exists)
    qr_code_url = "/static/images/upi_qr.png"

    # ✅ Prepare data to send to HTML
    context = {
        "order": order,
        "upi_id": upi_id,
        "qr_code_url": qr_code_url,
        "amount": order.total_price,  # use calculated_total if needed
    }

    return render(request, "cafe_app/upi_payment.html", context)

from django.shortcuts import render, get_object_or_404
from .models import Order
def generate_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Fetch all items in this order using OrderItem
    order_items = order.orderitem_set.select_related('menu_item').all()

    item_details = []
    grand_total = 0

    for item in order_items:
        total = item.quantity * item.menu_item.price
        item_details.append({
            'name': item.menu_item.name,
            'price': item.menu_item.price,
            'quantity': item.quantity,
            'total': total
        })
        grand_total += total

    return render(request, 'cafe_app/generate_bill.html', {
        'order': order,
        'item_details': item_details,
        'grand_total': grand_total
    })
from django.shortcuts import redirect, get_object_or_404
from .models import Order

def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Optional: update order or bill model here
    # For example, mark the bill as paid

    # Redirect to bill page
    return redirect('generate_bill', order_id=order.id)
from django.shortcuts import render
from .models import Order, Bill, MenuItem

from .models import MenuItem

def dashboard(request):
    menu_items = MenuItem.objects.filter(available=True)  # Optional filter
    orders = Order.objects.all().order_by('-id')[:10]
    bills = Bill.objects.all().order_by('-id')[:10]
    context = {
        'menu_items': menu_items,
        'orders': orders,
        'bills': bills,
    }
    return render(request, 'cafe_app/dashboard.html', context)
from django.shortcuts import render, redirect
from .models import MenuItem
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_menu_item_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        MenuItem.objects.create(name=name, category=category, price=price, stock=stock)
        return redirect('dashboard')

    return render(request, 'cafe_app/add_item.html')
from django.shortcuts import render, redirect
from .models import MenuItem, Order, OrderItem
from decimal import Decimal

def place_order_view(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        payment_method = request.POST.get('payment_method')

        # Create a new order
        order = Order.objects.create(
            customer_name=customer_name,
            payment_method=payment_method
        )

        total = Decimal('0.00')

        # Loop through all menu items to get quantities
        for item in MenuItem.objects.filter(available=True):
            qty = request.POST.get(f'quantity_{item.id}')
            if qty and int(qty) > 0:
                quantity = int(qty)
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=quantity
                )
                total += item.price * quantity

        order.total_price = total
        order.save()

        return redirect('order_success', order_id=order.id)

    # If GET request, show menu
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'cafe_app/place_order.html', {'menu_items': menu_items})

from django.shortcuts import get_object_or_404, render, redirect
from .models import Order, OrderItem, Bill

def generate_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Get order items
    order_items = OrderItem.objects.filter(order=order)

    # Calculate total
    total_amount = sum(item.total_price for item in order_items)

    # Check if bill already exists
    bill, created = Bill.objects.get_or_create(
        order=order,
        defaults={
            'total_amount': total_amount,
            'payment_method': order.payment_method
        }
    )

    # Optional: update bill if already created and values changed
    if not created:
        bill.total_amount = total_amount
        bill.payment_method = order.payment_method
        bill.save()

    return render(request, 'cafe_app/bill.html', {
        'order': order,
        'order_items': order_items,
        'bill': bill
    })

def bill_view(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'cafe_app/bill.html', context)
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Order, OrderItem

def export_bill_pdf(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.orderitem_set.all()
    template_path = 'cafe_app/pdf_template.html'
    context = {'order': order, 'order_items': order_items}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="bill_{order_id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had errors <pre>' + html + '</pre>')
    return response

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Order, Bill, MenuItem

def dashboard_view(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # Sales summary
    bills_today = Bill.objects.filter(generated_at__date=today)
    bills_week = Bill.objects.filter(generated_at__date__gte=week_ago)
    total_sales_today = sum(b.total_amount for b in bills_today)
    total_sales_week = sum(b.total_amount for b in bills_week)
    total_sales_all_time = sum(b.total_amount for b in Bill.objects.all())

    # Low stock items
    low_stock_items = MenuItem.objects.filter(stock__lte=5)

    # Order count
    total_orders = Order.objects.count()

    # ✅ Proper context defined
    context = {
        'sales_today': total_sales_today,
        'sales_week': total_sales_week,
        'total_sales': total_sales_all_time,
        'low_stock_items': low_stock_items,
        'total_orders': total_orders,
    }

    return render(request, 'cafe_app/dashboard.html', context)
from django.db.models import Sum
from django.shortcuts import render
from .models import Order, MenuItem

def dashboard_view(request):
    total_orders = Order.objects.count()

    # ✅ Sum only the total_price field (stored in database)
    total_sales = sum(order.total_price for order in Order.objects.all())

    total_items = MenuItem.objects.count()

    context = {
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_items': total_items,
    }

    return render(request, 'cafe_app/dashboard.html', context)
