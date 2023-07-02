from currencies.models import CurrencyHistory
from project.api_base_client import APIBaseClient


class BinanceCrypto(APIBaseClient):
    base_url = 'https://api.binance.com/api/v3/ticker/price'

    def _prepare_data(self) -> list:
        """
        [
            {"symbol":"BTCUSDT","price":"29198.29000000"},
            {"symbol":"ETHUSDT","price":"1905.35000000"},
            ...
        ]
        [{'code': 'BTCUSDT', "price":"29198.29000000",
        "price":"29198.29000000"},]
        :return: dict
        """

        self._request(
            'get',

        )
        results = []
        if self.response:
            for i in self.response.json():
                if i['symbol'] == 'BTCUSDT' or i['symbol'] == 'ETHUSDT':
                    results.append({
                        'code': i['symbol'],
                        'buy': i['price'],
                        'sale': i['price'],
                        'bank_name': 'Binance'
                    })
        return results

    def save(self):
        results = []
        for i in self._prepare_data():
            results.append(
                CurrencyHistory(
                    **i
                )
            )
        if results:
            CurrencyHistory.objects.bulk_create(results)


binance_client = BinanceCrypto()
