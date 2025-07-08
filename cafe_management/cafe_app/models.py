from django.db import models

# ✅ Menu Item Model
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('beverage', 'Beverage'),
        ('snack', 'Snack'),
        ('meal', 'Meal'),
        ('dessert', 'Dessert'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# ✅ Order Model
from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    payment_method = models.CharField(
        max_length=20,
        choices=[('Cash', 'Cash'), ('UPI', 'UPI')]
    )
    order_time = models.DateTimeField(auto_now_add=True)

    # ✅ Actual database field to avoid IntegrityError
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    # Optional: still allow dynamic calculation if needed
    @property
    def calculated_total(self):
        return sum(item.total_price for item in self.orderitem_set.all())

# ✅ Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.pk:  # Only subtract stock on first save
            self.menu_item.stock -= self.quantity
            self.menu_item.save()
        super().save(*args, **kwargs)

# ✅ Bill Model
class Bill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=10)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill #{self.id} - Order #{self.order.id}"

