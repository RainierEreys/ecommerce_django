from ecommerce.models import Product, Order, OrderDetail
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
    order_details = serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'date_time',
            'order_details',
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
    
   
    
            
        