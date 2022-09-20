from distutils.command import upload
from tabnanny import verbose
from django.db import models

class category(models.Model):
    cat_name = models.CharField(verbose_name='Категория', max_length=100)
    comment = models.CharField(verbose_name='Коментарии', max_length=100, null=True)
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
    name = models.CharField(verbose_name='Название продукта', max_length=100)
    price = models.IntegerField(verbose_name='Цены')
    CATEGORY = (
        (1, 'Пицца'),
        (2, 'Бургер'),
        (3, 'Стрипсы'),
        (4, 'Напитки'),
        (5, 'Прочи'),
    )
    category = models.IntegerField(verbose_name='Категория', choices=CATEGORY)
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