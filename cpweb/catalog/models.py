from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    def __str__(self):
        return str(self.user.first_name)

class Order(models.Model):
    number = models.IntegerField()
    due_date = models.DateField(null=True)
    price = models.FloatField(null=True)
    status = models.CharField(max_length=20)
    id_user = models.ForeignKey(User,to_field='id',on_delete= models.PROTECT)
    order_date = models.DateField(null=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])


class OrderComposition(models.Model):
    id_order = models.ForeignKey('Order', to_field='id',on_delete= models.PROTECT)
    quantity = models.IntegerField()
    id_product = models.ForeignKey('Product',to_field='id', on_delete=models.PROTECT)
    filling = models.CharField(max_length=100, default='')
    price = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    create_time = models.CharField(max_length=20)
    img = models.ImageField(upload_to='media', null=True)
    count = models.CharField(max_length=20, null=True)
    description = models.TextField(default='')
    status = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])


class Taste(models.Model):
    filling = models.CharField(max_length=100)
    id_product = models.ForeignKey('Product',to_field='id', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])
