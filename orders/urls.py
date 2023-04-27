from django.urls import path, re_path

from orders.views import CartView, CartActionView

urlpatterns = [
    path('order/', CartView.as_view(), name='order'),
    re_path(r'order/(?P<action>add|remove|clear|pay)/',  # маршрут для обработки запросов с корзиной
            CartActionView.as_view(),
            name='order_action'),
]
