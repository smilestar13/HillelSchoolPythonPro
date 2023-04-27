from django.urls import path, re_path

from orders.views import CartView, CartActionView

urlpatterns = [
    path('order/', CartView.as_view(), name='order'),
    # маршрут для обработки запросов с корзиной
    re_path(r'order/(?P<action>add|remove|clear|pay)/',
            CartActionView.as_view(),
            name='order_action'),
]
