# cafe_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('menu/', views.menu_view, name='menu'),
    path('inventory/', views.inventory_view, name='inventory'),
path('place-order/', views.place_order_view, name='place_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('bill/<int:order_id>/', views.bill_view, name='bill'),
path('generate-bill/<int:order_id>/', views.generate_bill, name='generate_bill'),
    path('payment/<int:order_id>/', views.upi_payment_view, name='initiate_upi_payment'),
    # urls.py
   path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('confirm-payment/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
      path('dashboard/', views.dashboard_view, name='dashboard'),
          path('add-item/', views.add_menu_item_view, name='add_item'),
              path('export-bill/<int:order_id>/', views.export_bill_pdf, name='export_bill_pdf'),


]


