import requests
import json


variables = []


class ConvertionException(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def get_price():
        url = f'https://api.exchangerate.host/latest?base={variables[0]}&symbols={variables[1]}&amount={variables[2]}'
        page = requests.get(url)
        texts = json.loads(page.content)['rates'][variables[1]]
        return texts
