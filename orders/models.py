from django.db import models
from django.contrib.auth.models import User
from product.models import FoodItem

class Order(models.Model):
    CHOICES_TYPE = [
        ('Individual', 'Individual'),
        ('Family', 'Family'),
        ('Event', 'Event'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    delivery_address = models.TextField()
    dish_counter = models.PositiveIntegerField(default=1)
    request_type = models.CharField(max_length=20, choices=CHOICES_TYPE, default='Individual')
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"