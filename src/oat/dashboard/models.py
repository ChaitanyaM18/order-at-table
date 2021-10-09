from django.db import models
from datetime import datetime

# Create your models here.

class QRModel(models.Model):
    image_path = models.CharField(max_length=20)
    image_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.image_path} Image'


class Category(models.Model):
    category_title = models.CharField(max_length=200)
    category_image = models.ImageField(null=True, blank=True, upload_to='uploads/category/',)

    published = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category_title}"


class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    menu_image = models.ImageField(null=True, blank=True, upload_to='uploads/menu/',)
    description = models.TextField()

    published = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dish_name}"
