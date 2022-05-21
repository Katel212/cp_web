from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='home'),
    path('item/<int:id_item>', views.item, name='item'),
    path('successful_add', views.successful_add, name='successful_add'),
    path('profile', views.profile, name='profile'),
    path('cart', views.cart, name='cart')
]

# urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
