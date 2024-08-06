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
    
    def validate(self, data):
        order = data.get('order')
        
        registros_mismo_order = OrderDetail.objects.filter(order=order)
        
        if registros_mismo_order.exists():
            print('registros iguales')
        
        
    # def get_order_details(self, id):
    #     order_details = OrderDetail.objects.filter(order=id)
    #     return OrderDetailSerializer(order_details, many=True).data
    
    # def get_total(self):
    #     order_detail_price = OrderDetail.objects.filter(order=id)   
    
            
        