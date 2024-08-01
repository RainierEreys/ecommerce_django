from rest_framework.routers import DefaultRouter
from ecommerce.views import ProductViewSet, OrderViewSet, OrderDetailViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r'productos', ProductViewSet, basename='producto')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'orderdetails', OrderDetailViewSet, basename='orderdetail')


urlpatterns = [
    path('', include(router.urls)),
]



