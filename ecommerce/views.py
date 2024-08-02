from django.shortcuts import render
from rest_framework import viewsets, permissions
from ecommerce.serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer
from ecommerce.models import Product, Order, OrderDetail

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    
    

