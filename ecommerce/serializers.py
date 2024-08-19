from ecommerce.models import Product, Order, OrderDetail
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.response import Response

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
    
    def create(self, validated_data):
        details = validated_data.pop('details', [])
        order = super().create(validated_data)
        
        
        orders_to_create = []
        for detail in details:
            product = Product.objects.get(name=detail['product'])
            print(f'stock: {product.stock} y el quantity es {detail["quantity"]}')
            
            if product.stock >= detail['quantity']:
                product.stock -= detail['quantity']
                product.save()
                orders_to_create.append(detail)
                print(orders_to_create)
            else:
                raise ValidationError({'la cantidad del producto: {product} no esta disponible'})
        
        OrderDetail.objects.bulk_create(
            [
                OrderDetail(**detail, order=order) for detail in orders_to_create
            ]
        )
        
        return order
    
    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        
        order_details_to_update = []
        for detail_data in details:
            # Para obtener el producto
            product = Product.objects.get(name=detail_data['product']) 

            # Para buscar o crear OrderDetail
            print(product.stock)
            order_detail, created = OrderDetail.objects.get_or_create(
                order=instance,
                product=product,
                defaults={
                    'quantity': detail_data['quantity'],
                }
            )

            # Para actualizar los atributos del objeto OrderDetail
            for attr, value in detail_data.items():
                # Para evitar actualizar estos campos
                #si los atributos no son 'product' ni 'order' 
                # (que no conviene modificarlos), entonces asigna valor nuevo valor
                # en este caso seria 'quantity'
                if attr not in ['product', 'order']:  
                    setattr(order_detail, attr, value)

            if product.stock >= detail_data['quantity']:
                product.stock -= detail_data['quantity']
                product.save()
                order_details_to_update.append(order_detail)
            else:
                raise ValidationError({{f'La cantidad solicitada para el {product} es menor a la cantidad que queda disponible'}})
           
        # Campos a actualizar
        fields = ['product', 'quantity']
        print(order_details_to_update)
        if not order_details_to_update:
            raise ValidationError({'No se realizaron cambios en los detalles del pedido.'})
        OrderDetail.objects.bulk_update(order_details_to_update, fields) 
        return instance
        
        
        
            
        