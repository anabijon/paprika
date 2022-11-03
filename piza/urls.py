from django.contrib import admin
from django.urls import path, include
from piza.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-product/', ProductCreateView.as_view()),
    path('product-list/', PizaListView.as_view()),
    path('category/', CategoryListView.as_view()),
    path('detail-product/<int:pk>/', PizaDetailView.as_view()),
    path('product-ct_id/<int:category>/', PizaCategoryView.as_view()),
    path('basket-list/', BasketList.as_view()),
    path('orders-list/', OrdersList.as_view()),
    path('add-contact-info/', AddContactView.as_view()),
    path('add-orders/', AddOrders.as_view()),
    path('profil/', Profil.as_view()),
]