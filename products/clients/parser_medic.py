import logging
from bs4 import BeautifulSoup
import requests
from project.api_base_client import APIBaseClient

logger = logging.getLogger(__name__)


class Medic(APIBaseClient):
    base_url = "https://medik8.ua/catalog/kits"

    def _prepare_data(self) -> list:
        self._request(
            'get',
        )
        results = []
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            category = soup.find('h1').text.replace('\r', '').replace('\n', '').strip()  # noqa
            for item in soup.find_all('div',
                                      class_='collection-item product-item'):
                start_url = 'https://medik8.com.ua/'
                try:
                    product_url = start_url + \
                                  item.find_all('a')[0].get('href')
                    product_response = requests.get(product_url)
                    product_soup = BeautifulSoup(product_response.content,
                                                 'html.parser')
                    desc_text = product_soup.find('div', class_='description is-hidden js-read-description').text.replace('\n', '').replace('\r', '').replace('\xa0', ' ').strip()  # noqa
                    desc_trigger = desc_text.find(' У наборі:')
                    is_active = item.find_all('a')[2].text.replace('\r', '').replace('\n', '').strip()  # noqa
                    if is_active == "В кошик":
                        results.append({
                            'sku': item.find_all('a')[2].get('item_id'),
                            'category': category,
                            'image': start_url + item.find('img').get('src'),
                            'name': item.find_all('a')[1].text,
                            'description': desc_text[:desc_trigger],
                            'price': item.find('p').text.split()[0]
                        })
                except Exception as err:
                    logger.error(err)
        return results

    def parse(self) -> list:
        return self._prepare_data()

    def get_image(self, url):
        self._request(
            'get',
            url=url
        )
        return self.response


parser_client = Medic()
