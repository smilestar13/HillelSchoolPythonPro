from orders.models import Order


class GetCurrentOrderMixin:  # Создаем миксин для получения текущего заказа пользователя

    def get_object(self):
        """Метод для получения текущего заказа"""
        return Order.objects.get_or_create(
            is_active=True,
            is_paid=False,
            user=self.request.user
        )[0]