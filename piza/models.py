import datetime
from distutils.command import upload
from tabnanny import verbose
from django.db import models
from .db import post_pizaproduct_order, get_orders_list, post_add_orders, get_profil_list
from authentification.auth_decorators import auth_required


class category(models.Model):
    cat_name = models.CharField(verbose_name='Категория', max_length=100)
    comment = models.CharField(verbose_name='Коментарии', max_length=100, null=True)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)
    image = models.ImageField(upload_to = "category_icon/%Y/%m/%d", verbose_name='Значок', null=True)
    STATUS = (
            (1, 'Активна'),
            (2, 'Отключена'),
        )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS)

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Products(models.Model):
    name = models.CharField(verbose_name='Название продукта', max_length=100, unique=True)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)
    CATEGORY_NMAE = (
        (1, 'Пицца'),
        (2, 'Бургер'),
        (3, 'Стрипсы'),
        (4, 'Напитки'),
        (5, 'Прочи'),
    )
    category = models.IntegerField(verbose_name='Категория', choices=CATEGORY_NMAE)
    #category = models.ForeignKey(category, on_delete=models.PROTECT, null=True, verbose_name='Продукт',)
    image = models.ImageField(upload_to = "photos/%Y/%m/%d", verbose_name='Фото')
    Ingredients = models.CharField(verbose_name='Ингридиенд', max_length=300)
    STATUS = (
        (1, 'Активна'),
        (2, 'Отключена'),
    )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'

class ProductItem(models.Model):
    product = models.ForeignKey(to=Products, to_field='name', related_name='ProductItem', on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    volume_name = models.CharField(verbose_name='Объем/размер', max_length=5)

    def __str__(self):
        return  self.product_id
    def get_cost(self):
        return f'{self.product} {self.price}'

class customers(models.Model):
    name = models.CharField(verbose_name='ФИО клиент', max_length=100)
    phone = models.CharField(verbose_name='Номер телефон', max_length=12)
    device_token = models.CharField(verbose_name='Устройства', max_length=250)
    adress = models.CharField(verbose_name='Адресс', max_length=250)
    comment = models.CharField(verbose_name='Коментарии', max_length=100, null=True)
    STATUS = (
        (1, 'Активна'),
        (2, 'Отключена'),
    )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS)

    class Meta:
        verbose_name = 'Клиенты'
        verbose_name_plural = 'Клиенты'
        ordering = ['-id']

class sales_report(models.Model):
    phone = models.CharField(verbose_name='Номер телефон', max_length=12)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True, verbose_name='Продукт',)
    product_price = models.IntegerField(verbose_name='Сумма')
    date = models.DateTimeField(verbose_name='Время продаж', max_length=15)
    delivery_address = models.CharField(verbose_name='Адресс доставки', max_length=200)
    comment = models.CharField(verbose_name='Коментарии', max_length=100, null=True)
    STATUS = (
        (1, 'Продан'),
        (2, 'Отменен'),
    )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS)

    class Meta:
        verbose_name = 'Отчет по продаж'
        verbose_name_plural = 'Отчет по продаж'
        ordering = ['-date']

class TestTable(models.Model):
    id_test = models.IntegerField(blank=True, null=True)
    text = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Тестовая таблица'
        verbose_name_plural = 'Тестовая таблица'
        managed = False
        db_table = 'test_table'

class orders(models.Model):
    phone = models.CharField(verbose_name='Номер телефон', max_length=12)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, null=True, verbose_name='Продукт')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время создание заказа', max_length=15)
    time_delivery = models.DateTimeField(verbose_name='Время доставки', max_length=15)
    adress = models.CharField(verbose_name='Адрес доставки', max_length=100, null=True)
    comment = models.CharField(verbose_name='Коментарии', max_length=100, null=True)
    paid = models.IntegerField(verbose_name='Цена')
    order_id = models.IntegerField(verbose_name='Номер заказ')

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
        ordering = ['order_id']

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(orders, related_name='items', on_delete=models.PROTECT)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
 
#@auth_required(token=False)
def pizaproduct_order(request, category):
    return post_pizaproduct_order(request, category)

class order_status(models.Model):
    status_name = models.CharField(verbose_name='Статус', max_length=50)

class DeliveryInfo(models.Model):
    delivery_time = models.DateTimeField(verbose_name='Время доставки')
    adress = models.CharField(verbose_name='Адрес доставки', max_length=100, null=True)
    comment = models.CharField(verbose_name='Коментарии', max_length=100, null=True)
    cre_date = models.DateTimeField(auto_now_add=True, verbose_name='Время создание заказа', max_length=15)
    phone = models.CharField(verbose_name='Телефон', max_length=12, null=True)
    #phone = models.ForeignKey(Products, related_name='InfoDelivery', on_delete=models.PROTECT)
    STATUS = (
        (0, 'Карзина'),
        (1, 'Самовоз'),
        (2, 'В процессе'),
        (3, 'На доставке'),
        (4, 'Отказ'),
    )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS)
    #order_id = models.IntegerField(verbose_name='ID заказ')
    order = models.ForeignKey(orders, related_name='InfoDelivery', on_delete=models.PROTECT)
    

class contact_info(models.Model):
    phone = models.CharField(verbose_name='Номер телефон', max_length=12)
    name = models.CharField(verbose_name='ФИО', max_length=50)
    adress = models.CharField(verbose_name='Адрес', max_length=100)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'
        ordering = ['id']

@auth_required(token_only=False)
def orders_list(request, msisdn):
    return get_orders_list(msisdn)

@auth_required(token_only=False)
def add_orders_post(request, msisdn, delivery_status, delivery_time, delivery_address, delivery_comment, product):
    return post_add_orders(msisdn, delivery_status, delivery_time, delivery_address, delivery_comment, product)

@auth_required(token_only=False)
def profil_list(request, msisdn):
    return get_profil_list(msisdn)