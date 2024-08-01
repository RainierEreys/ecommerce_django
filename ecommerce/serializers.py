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
        
    # def get_order_details(self, id):
    #     order_details = OrderDetail.objects.filter(order=id)
    #     return OrderDetailSerializer(order_details, many=True).data
    
    # def get_total(self):
    #     order_detail_price = OrderDetail.objects.filter(order=id)   
    
            
        