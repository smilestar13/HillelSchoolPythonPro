from django import template

from currencies.models import CurrencyHistory

register = template.Library()


@register.filter
def multiply_price_by_usd_rate(price):
    usd_rate = CurrencyHistory.get_usd_rate()
    return price * usd_rate.__round__()
