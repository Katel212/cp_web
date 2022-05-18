from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render

from .forms import TasteForm
from .models import Product, Order, OrderComposition
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
    else:
        num = num.number +1
    order_id = Order.objects.get_or_create(id_user=user_id, status='0', number=num)[0]

    OrderComposition.objects.create(id_order=order_id, id_product = product, **tastes_form.cleaned_data)
    return HttpResponseRedirect('catalog/successful_add')


def successful_add(request):
    return HttpResponse('thanks')

@login_required
def profile(request):
    print(request.user.is_authenticated)
    return render(request, 'catalog/profile.html')
