from django.db import models
from .utils import getVerdeValue
from datetime import datetime
import requests

# Create your models here.
class ValueDolar(models.Model):
    date_time = models.DateField(auto_now_add=True)
    value = models.FloatField(verbose_name='Valor Dolar')
    
    @classmethod
    def get_or_update_value(cls):
        value_dolar, created = cls.objects.get_or_create(id=1)
        fecha_hoy = datetime.now()
        # print(fecha_hoy.date())
        if created or value_dolar.value is None or value_dolar.date_time != fecha_hoy.date():
            # Si se creó o el valor es None, actualiza el valor
            value_dolar.value = getVerdeValue()
            value_dolar.save()
        return value_dolar.value
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
    
    def __str__(self):
        return self.name
   
class Order(models.Model):
    date_time = models.DateField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = sum(detail.product.price * detail.quantity for detail in self.details.all())
        return total
    
    @property
    def get_total_usd(self):
        try:
            value_dolar = ValueDolar.get_or_update_value()
            total_en_bs = self.get_total
            total_en_usd = total_en_bs * value_dolar
            return total_en_usd
        except ValueError as e:
            return {'error': 'no se pudo obtener el valor'}
        
        
    
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details", default=1)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
