from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.db.models import Count
from rest_framework.response import Response
from product.models import Product, Category
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer
from rest_framework.views import APIView

class ViewProducts(APIView):
    def get(self,request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products,many=True,context={'request':request})
        return Response(serializer.data)
    def post(self,request):
        serializer = ProductSerializer(data=request.data) #deserializer
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewSpecificProduct(APIView):
    def get(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)   

    def put(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    def delete(self,request,id):
        product = get_object_or_404(Product,pk=id)

        copy_of_product = product
        product.delete()
        serializer= ProductSerializer(copy_of_product)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

class ViewCategories(APIView):
    def get(self,request):
        categories = Category.objects.annotate(product_count = Count('products'))
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CategorySerializer(data=request.data) #deserializer
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class ViewSpecificCategory(APIView):
    def get(self,request,pk):
        category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
  
    def put(self,request,pk):
        category = get_object_or_404(Category.objects.annotate(product_count = Count('products')),pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request,pk):
        category = get_object_or_404(Category,pk=pk)

        copy_of_category = category
        category.delete()
        serializer= CategorySerializer(copy_of_category)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
