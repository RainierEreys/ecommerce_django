from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField()
    price = models.IntegerField()
    stock = models.IntegerField()
    
class Order(models.Model):
    date_time = models.DateField(auto_now_add=True)
    
class OrderDetail(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product = models.ManyToManyField(Product, on_delete=models.CASCADE)
    