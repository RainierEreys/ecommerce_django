from django.shortcuts import render
from rest_framework import viewsets, permissions
from ecommerce.serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer, UserSerializer
from ecommerce.models import Product, Order, OrderDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Sum
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

    
    # valores_vistos = set()
    # valores_repetidos = set()
    
    # def list(self, request, *args, **kwargs):
    #     query = OrderDetail.objects.all()
    #     for index, datos in enumerate(query):
    #         if datos.order_
    #         print(f"{index} {datos.id} {datos.order_id}")
    #     return Response({})
    
    
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
        
    
class ConsumoApi(APIView):
    def get(self, request, *args, **kwargs):
        #hago la solicitud
        response = requests.get("")
        
        if response.status_code == 200:
            tareas = response.json()
            return Response(tareas, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':'no se ha logrado la conexion'}, status=status.HTTP_400_BAD_REQUEST)
    

