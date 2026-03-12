from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from order.models import Cart,CartItem,Order,OrderItem
from order.serializers import CartSerializer,CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, EmptySerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
# Create your views here.
from rest_framework.response import Response
from rest_framework import status

class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()

        return Cart.objects.prefetch_related(
            'items__product'
        ).filter(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     if not serializer.is_valid():
    #         print(serializer.errors)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # def perform_create(self, serializer):
    #     print('user:', self.request.user)
    #     serializer.save(user=self.request.user)



class CartItemViewSet(ModelViewSet):
    # queryset = CartItem.objects.all()
    # serializer_class = CartItemSerializer 
    http_method_names=['get','post','patch','delete']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self,'swagger_fake_view', False):
            return context
        return {'cart_id': self.kwargs['cart_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        # return CartItem.objects.select_related('product').filter(cart_id = self.kwargs['cart_pk'])
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs.get('cart_pk'))
    

class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','patch','delete','head','options']
    
    @action(detail=True, methods=['post'])
    def cancel(self,request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status':'order cancled'})
    
    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order,data = request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"status updated successfully to {request.data['status']}"})

    # def get_permissions(self):
    #     if self.request.method == 'DELETE':
    #         return [IsAdminUser()]
    #     return [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['update_status','destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user= self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        # if self.request.method == 'POST':
        #     return CreateOrderSerializer
        if self.action == 'create':
            return CreateOrderSerializer
        # elif self.request.method == 'PATCH':
        #     return UpdateOrderSerializer
        elif self.action == 'update_status':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user':self.request.user}