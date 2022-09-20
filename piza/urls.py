from django.contrib import admin
from django.urls import path, include
from piza.views import *

urlpatterns = [
    path('piza/create/', ProductCreateView.as_view()),
    path('product/', PizaListView.as_view()),
    path('category/', CategoryListView.as_view()),
    path('piza/detail/<int:pk>/', PizaDetailView.as_view())
]
