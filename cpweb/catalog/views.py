from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.urls import reverse

from .forms import TasteForm
from .models import Product, Order, OrderComposition, MyUser
from django.contrib.auth.models import User


def index(request):
    return render(request, "catalog/home.html")


def item(request, id_item):
    form_data = request.POST if request.method == "POST" else None
    tastes_form = TasteForm(form_data)
    product = Product.objects.get(id=id_item)
    context = {'product': product, 'form_taste': tastes_form}

    if request.method != "POST" or not tastes_form.is_valid():
        return render(request, "catalog/item.html", context)
    print(request.user.is_authenticated)

    user_id = User.objects.get(id=request.user.id)
    num = Order.objects.order_by('number').last()
    if num is None:
        num = 1
    elif num.status == '0':
        num = num.number
    else:
        num = num.number + 1
    order_id = Order.objects.get_or_create(id_user=user_id, status='0', number=num)

    order_comp = OrderComposition.objects.filter(id_order=order_id[0], id_product = id_item)
    if order_comp.count() !=0:
        order_comp = OrderComposition.objects.get(id_order=order_id[0], id_product = id_item)
        order_comp.quantity +=1
        order_comp.save()
    else:
        OrderComposition.objects.create(id_order=order_id[0], id_product=product, **tastes_form.cleaned_data)
    return render(request, 'catalog/succesful_add.html', {'product': product})


def successful_add(request):
    return render(request, 'catalog/succesful_add.html')


@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    myuser = MyUser.objects.get(user=user)
    orders = Order.objects.filter(id_user=user)
    compositions = OrderComposition.objects.filter(id_order__in=orders)
    product_set = compositions.values_list('id_product', flat=True)
    products = Product.objects.filter(id__in=product_set)

    context = {'user': user, 'my_user': myuser, 'orders': orders, 'compositions': compositions, 'products': products}
    return render(request, 'catalog/profile.html', context=context)


def cart(request):
    user = User.objects.get(id=request.user.id)
    orders = Order.objects.get(id_user=user, status='0')
    compositions = OrderComposition.objects.filter(id_order__in=orders)
    product_set = compositions.values_list('id_product', flat=True)
    products = Product.objects.filter(id__in=product_set)
    sum = 0
    for c in compositions:
        sum += c.price * c.quantity
    context = {'user': user, 'orders': orders, 'compositions': compositions, 'products': products, 'sum': sum}
    return render(request, 'catalog/cart.html', context=context)
