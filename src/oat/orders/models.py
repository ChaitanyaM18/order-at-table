from django.db import models
from datetime import datetime


class UserDetails(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField(max_length=200)
    user_contact = models.CharField(max_length=15)
    address = models.TextField()
    user_table_no = models.CharField(max_length=15)

    published = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_name}"


class UserOrder(models.Model):
    username = models.CharField(max_length=200, default='') #who placed the order
    table_number = models.CharField(max_length=200, default='') #who placed the order
    order = models.TextField() #this will be a string representation of the cart from localStorage
    price = models.DecimalField(max_digits=6, decimal_places=2) #how much was the order
    time_of_order  = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length=10, default='')

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"

    def get_foo(self):
        return json.loads(self.foo)

class GetUserReview(models.Model):
    ratings = models.CharField(max_length=5)
    table_no = models.CharField(max_length=50)
    username = models.CharField(max_length=500)
    comments = models.TextField()

    def __str__(self):
        return f"{self.ratings}"


class AddsView(models.Model):
    title = models.CharField(max_length=200, default='')
    video_or_image = models.FileField(null=True, blank=True, upload_to='uploads/videos/',)

    published = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
