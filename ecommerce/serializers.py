from models import Product, Order, OrderDetail
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'stock',
            ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'date_time',
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