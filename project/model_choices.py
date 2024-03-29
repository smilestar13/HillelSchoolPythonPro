from django.db.models import IntegerChoices, TextChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'Value'
    PERCENT = 1, 'Percent'


class Currencies(TextChoices):
    UAH = 'UAH', 'UAH'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    BTC = 'BTCUSDT', 'BTC'
    ETH = 'ETHUSDT', 'ETH'


class ProductCacheKeys(TextChoices):
    PRODUCTS = 'products', 'Products all'


class FeedbackCacheKeys(TextChoices):
    FEEDBACKS = 'feedbacks', 'Feedbacks all'
