from django.shortcuts import render
from rest_framework import generics, status
from piza.serializers import ProductDetailSerializer, ProductListSerializer, ProductCategorySerializer, CategoryListSerializer, OrderDetailSerializer, OrderItemDetailSerializer, ProductItemSerializer, AddContactSerializer, PizaOrder, DeliverySerializer
from piza.models import Products, category, ProductItem, pizaproduct_order, orders, add_orders_post, profil_list
from rest_framework.views import APIView
from rest_framework.response import Response
from piza.utils import filterResponse
import piza.serializers as serializer
import json
from authentification.auth_decorators import auth_required

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

class PizaCategoryView(APIView):
    def get(self, request, category):
        data = Products.objects.filter(category=category).all()
        productinfo = ProductDetailSerializer(data=data, many=True)
        productinfo.is_valid()
        return Response({"products": productinfo.data})

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderDetailSerializer

class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemDetailSerializer

class BasketList(APIView):
    def get(self, request):
        data = orders.objects.filter(status=1).all()
        BasketInfo = DeliverySerializer(data=data, many=True)
        BasketInfo.is_valid()
        return Response({"BasketOrders": BasketInfo.data})

class PizaOrders(APIView):
    def post(self, request):
        validation = serializer.PizaOrder(data=request.data)
        if validation.is_valid(raise_exception=True):
            return filtering(
                pizaproduct_order(
                    request, 
                    phone=validation.data['phone']
                    )
            )
        else:
            return Response({"message":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class AddContactView(generics.CreateAPIView):
    serializer_class = AddContactSerializer

class OrdersList(APIView):
    # def get(self, request):
    #     resp=orders_list(request)
    #     return Response(resp)
    def get(self, request):
        resp=orders_list(request)
        if 'err_code' in resp.keys():
            if resp['err_code'] !=0:
                content = {
                    'result': -1,
                    'err_msg': 'Err resp test',
                }
                return Response({"message":"You didn't have orders"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return filterResponse(
                    resp
                )
        else:
            return filterResponse(resp)

class AddOrders(APIView):        
    def post(self, request):
        validation = serializer.addorders(data=request.data)
        if validation.is_valid(raise_exception=True):
            r=add_orders_post(
                    request, 
                    delivery_status = validation.data['delivery_status'],
                    delivery_time = validation.data['delivery_time'],
                    delivery_address = validation.data['delivery_time'],
                    delivery_comment = validation.data['delivery_comment'],
                    product = validation.data['product']
                )
            if 'err_code' in r.keys():
                if r['err_code']!=0:
                    content = {
                        'err_code': r['err_code'],
                        'err_msg': r['err_msg'],
                        }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return filterResponse(
                        r
                    )
            elif  r['un_authorized']==True:
                content = {
                        'err_code': -400,
                        'err_msg': "You are not authorized",
                        }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('===>>> ', r)
                return Response('Bad request', status=status.HTTP_400_BAD_REQUEST)

class Profil(APIView):
    def get(self, request):
        resp=profil_list(request)
        if 'err_code' in resp.keys():
            if resp['err_code'] !=0:
                content = {
                    'result': -1,
                    'err_msg': 'Err resp test',
                }
                return Response({"message":"Delivery information about Sun not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return filterResponse(
                    resp
                )
        else:
            return filterResponse(resp)