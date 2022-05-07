from django.db import models
from django.urls import reverse


class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.login

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Order(models.Model):
    number = models.IntegerField()
    due_date = models.DateField()
    price = models.FloatField()
    status = models.CharField(max_length=20)
    id_user = models.ForeignKey('User', models.PROTECT)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])


class OrderComposition(models.Model):
    id_order = models.ForeignKey('Order', models.PROTECT)
    quantity = models.IntegerField()
    id_product = models.ForeignKey('Product', on_delete=models.PROTECT)

    def __str__(self):
        return self.id


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    create_time = models.CharField(max_length=20)
    img = models.ImageField(null=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])


class Taste(models.Model):
    filling = models.CharField(max_length=50)
    img = models.ImageField(null=True)
    id_product = models.ForeignKey('Product', on_delete=models.PROTECT)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])
