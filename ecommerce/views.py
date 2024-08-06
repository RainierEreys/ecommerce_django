from django.shortcuts import render
from rest_framework import viewsets, permissions
from ecommerce.serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer, UserSerializer
from ecommerce.models import Product, Order, OrderDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

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
    
    def list(self, request, *args, **kwargs):
        query = OrderDetail.objects.all()
        for index, datos in enumerate(query):
            print(f"{index} {datos.id} {datos.order_id}")
        return Response({})
    
    
class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    
    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     return Response({})
    
    
    
    

