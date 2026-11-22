from django.db import models


class FoodItem(models.Model):
  choice = [
      ('Pastries','Pastries'),
      ('Salad','Salad'),
      ('Fast Food','Fast Food'),
      ('Main courses', 'Main courses'),
      ('Soups','Soups'),
      ('Drinks','Drinks'),
  ]
  category = models.CharField(max_length=100, choices=choice)
  name = models.CharField(max_length=200)
  description = models.TextField(blank=True, null=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  image = models.ImageField(upload_to='food_images/', blank=True, null=True)
  image2 = models.ImageField(upload_to='food_images/', blank=True, null=True)
  image3 = models.ImageField(upload_to='food_images/', blank=True, null=True)
  image4 = models.ImageField(upload_to='food_images/', blank=True, null=True)
  rating = models.PositiveIntegerField(default=5)
  reviews_count = models.PositiveIntegerField(default=128)
  is_chef_special = models.BooleanField(default=False)
  def __str__(self):
    return self.name