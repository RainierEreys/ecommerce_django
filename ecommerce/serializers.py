from ecommerce.models import Product, Order, OrderDetail
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password'
        ]
 

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'stock',
            ]

class OrderDetailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = OrderDetail
        fields = [
            'id',
            'order',
            'quantity',
            'product',
        ]
        
    
    
    
    
class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'date_time',
            'details',
            ] 
    
        
    
            
        