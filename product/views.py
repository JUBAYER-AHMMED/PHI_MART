from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.db.models import Count
from rest_framework.response import Response
from product.models import Product, Category,Review
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend 
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly

from product.paginations import DefaultPagination

# from rest_framework.permissions import IsAdminUser , AllowAny
from api.permissions import IsAdminOrReadOnly, FullDjangoModelPermission

from product.permissions import IsReviewAuthorOrReadOnly
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category_id','price']
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    pagination_class = DefaultPagination
    search_fields = ['name','description', 'category__name']
    ordering_fields = ['price', 'updated_at']
    # permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAdminUser()]
    
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [FullDjangoModelPermission]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    
    

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get('category_id')

    #     if category_id is not None:
    #         queryset = Product.objects.filter(category_id = category_id)
    #     return queryset

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message':'Product with stock more than 10 could not be deleted'})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count = Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        # print("user:", self.request.user)
        serializer.save(user=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.filter(product_id = self.kwargs['product_pk'])
        return queryset

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}


# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('category').all()
#     serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}

# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'

    # def delete(self,request,id):
    #     product = get_object_or_404(Product,pk=id)
    #     if product.stock > 10:
    #         return Response({'message':'Product with stock more than 10 could not be deleted'})
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
        
    

# class ViewCategories(APIView):
#     def get(self,request):
#         categories = Category.objects.annotate(product_count = Count('products'))
#         serializer = CategorySerializer(categories,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = CategorySerializer(data=request.data) #deserializer
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class CategoryList(ListCreateAPIView):
#     queryset = Category.objects.annotate(product_count = Count('products'))
#     serializer_class = CategorySerializer

# class ViewSpecificCategory(APIView):
#     def get(self,request,pk):
#         category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
  
#     def put(self,request,pk):
#         category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=pk)
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    
#     def delete(self,request,pk):
#         category = get_object_or_404(Category,pk=pk)

#         copy_of_category = category
#         category.delete()
#         serializer= CategorySerializer(copy_of_category)
#         return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)


# class CategoryDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.annotate(product_count = Count('products'))
#     serializer_class = CategorySerializer
