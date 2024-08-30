from django.db import models
from .utils import getVerdeValue
from datetime import datetime
import requests

# Create your models here.
class ValueDolar(models.Model):
    date_time = models.DateField(auto_now_add=True)
    value = models.FloatField(verbose_name='Valor Dolar')
    _cached_value = None  # Variable de clase para almacenar el valor temporalmente

    @classmethod
    def create_new_value(cls):
        valor_monitor = getVerdeValue()
        return cls.objects.create(value=valor_monitor)

    @classmethod
    def get_latest_value(cls):
        print('latest_value')
        return cls.objects.last()

    @classmethod
    def get_or_create_latest_value(cls):
        if not hasattr(cls, '_cached_value'):
            print('no sucede')
            cls.create_new_value()
            cls._cached_value = cls.get_latest_value()
        else:
            print('sucede')
            cls._cached_value = cls.get_latest_value()
        return cls._cached_value
    
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
            print('hola')
            ultimo_valor = ValueDolar.get_latest_value()
            print(ultimo_valor)
            # print(ultimo_valor.exists())
            if ultimo_valor is None:
                print('estoy en if')
                valor_creado = ValueDolar.create_new_value()
                valor_consultado = valor_creado.value
                print(valor_consultado)
            elif ultimo_valor is None: 
                print('el valor es ninguno')
                valor_creado = ValueDolar.create_new_value()
                valor_consultado = valor_creado.value
                print(ultimo_valor.exists())
            else:
                print('estoy en else')
                valor_consultado = ValueDolar.get_latest_value().value
                print(valor_consultado)
            
            return ultimo_valor
        except ValueError as e:
            return {'error': 'no se pudo obtener el valor'}
        
        
    
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details", default=1)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
