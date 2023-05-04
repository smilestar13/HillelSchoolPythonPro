from django.db import models

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import Currencies


class CurrencyHistory(PKMixin):
    code = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=Currencies.UAH
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sale = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    bank_name = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=None
    )

    def __str__(self):
        return f"{self.code} - {self.buy} / {self.sale} ({self.bank_name}) - {self.created_at.strftime('%H:%M [%d.%m.%Y]')}"

    @staticmethod
    def get_usd_rate():
        usd_history = CurrencyHistory.objects.filter(code=Currencies.USD).latest('created_at')
        usd_rate = usd_history.sale
        return usd_rate
