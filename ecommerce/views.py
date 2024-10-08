from django.shortcuts import render
from rest_framework import viewsets, permissions
from ecommerce.serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer, UserSerializer
from ecommerce.models import Product, Order, OrderDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Sum
from django.db import transaction
import requests

from django.contrib.auth.models import User

# @api_view(["POST"])
# def register(request):
#     print(request.data)
#     return Response({})
class RegisterViewSet(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer_class = UserSerializer(data=request.data)
        if serializer_class.is_valid():
            validated_data = serializer_class.validated_data
            User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            
            return Response(serializer_class.data, status.HTTP_200_OK)
        return Response(serializer_class.errors, status.HTTP_400_BAD_REQUEST)
        
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_total(self):
        instance = self.get_object()
        

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        orderdetails = OrderDetail.objects.filter(order=order)
        print(orderdetails)
        
        for orderdetail in orderdetails:
            products_restore = Product.objects.get(name=orderdetail.product)
            products_restore.stock += orderdetail.quantity
            products_restore.save()
        
        orderdetails.delete()    
        print(f'holaholahola {order.id}')
        self.perform_destroy(order)
        
        if Order.objects.filter(id=order.id).exists():
            print(f'La orden {order.id} aún existe.')
        else:
            print(f'La orden {order.id} ha sido eliminada.')
            
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        instance.delete()
        print(f'Orden {instance.id} eliminada en perform_destroy')
    
    
class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        order = validated_data.get('order')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        
        stock_product = Product.objects.filter(name=product).first()
        if stock_product:
            if stock_product.stock > quantity:
                stock_product.stock -= quantity
                stock_product.save()
                order_detail, created = OrderDetail.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    order_detail.quantity += quantity
                    order_detail.save()
                    
                response_serializer = self.get_serializer(order_detail)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"insuficiente stock"}, status=status.HTTP_400_BAD_REQUEST)
        
    
# class ConsumoApi(APIView):
#     def get(self, request, *args, **kwargs):
#         #hago la solicitud
#         response = requests.get("https://pydolarve.org/api/v1/dollar?page=enparalelovzla")
        
#         if response.status_code == 200:
#             tareas = response.json()
#             valor_dolar = tareas['monitors']['enparalelovzla']['price']
#             return Response(valor_dolar, status=status.HTTP_200_OK)
#         else:
#             return Response({'mensaje':'no se ha logrado la conexion'}, status=status.HTTP_400_BAD_REQUEST)
    

