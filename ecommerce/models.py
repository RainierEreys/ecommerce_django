from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
  
class Order(models.Model):
    date_time = models.DateField(auto_now_add=True)
    

    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name="order_details", on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
    
    
    