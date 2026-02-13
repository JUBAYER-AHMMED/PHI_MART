from django.urls import path
from product import views
urlpatterns = [
    # path('',views.view_products,name = 'product-list'),
    # path('',views.ViewProducts.as_view(),name = 'product-list'),
    path('',views.ProductList.as_view(),name = 'product-list'),
    # path('<int:id>/', views.view_specific_product, name = 'specific'),
    # path('<int:id>/', views.ViewSpecificProduct.as_view(), name = 'specific'),
    path('<int:id>/', views.ProductDetails.as_view(), name = 'specific'),
]
