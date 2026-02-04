from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.db.models import Count

from rest_framework.response import Response
from product.models import Product, Category
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer

from rest_framework.views import APIView
# Create your views here.
# @api_view()
# def view_specific_product(request,id):
#     # product = Product.objects.all().first()
#     # print('id:', id)

#     product = Product.objects.get(pk=id)
#     # print('product:', product)

#     product_dict= {'id': product.id, 'name': product.name, 'price': product.price}
#     # return Response({"message":"Okay"})
#     return Response(product_dict)

# @api_view()
# def view_specific_product(request,id):
#     try:
#         product = Product.objects.get(pk=id)
#         product_dict= {'id': product.id, 'name': product.name, 'price': product.price}
#         return Response(product_dict)
#     except Product.DoesNotExist:
#         return Response({'message': "Product does not exist"},status=status.HTTP_404_NOT_FOUND)

# @api_view()
# def view_specific_product(request,id):
#     product = get_object_or_404(Product,pk=id)
#     product_dict= {'id': product.id, 'name': product.name, 'price': product.price}
#     return Response(product_dict)

@api_view(['GET','POST'])
def view_products(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products,many=True,context={'request':request})
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data) #deserializer
        # if serializer.is_valid():
        #     print(serializer.validated_data)
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET','PUT','DELETE'])
def view_specific_product(request,id):
    product = get_object_or_404(Product,pk=id)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    if request.method == 'DELETE':
        copy_of_product = product
        product.delete()
        serializer= ProductSerializer(copy_of_product)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)


@api_view()
def view_categories(request):
    categories =Category.objects.annotate(product_count = Count('products'))
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)
@api_view()
def view_specific_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)