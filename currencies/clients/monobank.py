from currencies.models import CurrencyHistory
from project.api_base_client import APIBaseClient


class MonoBank(APIBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def _prepare_data(self) -> list:
        """
        [
            {"currencyCodeA":840,"currencyCodeB":980,"date":1683151274,"rateBuy":36.65,"rateCross":0,"rateSell":37.4406},
            {"currencyCodeA":978,"currencyCodeB":980,"date":1683190574,"rateBuy":40.51,"rateCross":0,"rateSell":41.6997},
            {"currencyCodeA":978,"currencyCodeB":840,"date":1683190574,"rateBuy":1.099,"rateCross":0,"rateSell":1.111},
            ...
        ]
        [{'code': 'USD', "buy":"36.65","sale":"37.4406"},]
        :return: dict
        """

        self._request(
            'get',
            params={
                'json': '',
                'exchange': '',
                'coursid': 5
            }
        )
        results = []
        if self.response:
            for i in self.response.json():
                if i['rateBuy'] != 0 and i['rateSell'] != 0:
                    if i['currencyCodeA'] == 840 and i['currencyCodeB'] == 980:
                        results.append({
                            'code': 'USD',
                            'buy': i['rateBuy'],
                            'sale': i['rateSell'],
                            'bank_name': 'MonoBank'
                        })
                    elif i['currencyCodeA'] == 978 and i['currencyCodeB'] == 980:
                        results.append({
                            'code': 'EUR',
                            'buy': i['rateBuy'],
                            'sale': i['rateSell'],
                            'bank_name': 'MonoBank'
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


monobank_client = MonoBank()