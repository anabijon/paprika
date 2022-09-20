from django.shortcuts import render
from rest_framework import generics
from piza.serializers import ProductDetailSerializer, ProductListSerializer, CategoryListSerializer
from piza.models import Products, category

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer

class PizaListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Products.objects.all()

class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = category.objects.all()

class PizaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Products.objects.all()
