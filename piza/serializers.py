from rest_framework import serializers
from piza.models import Products, category

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('name', 'price', 'category', 'image', 'status')

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('cat_name', 'comment', 'image', 'status')