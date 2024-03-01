import json

import requests

from Currencies import currencies


class ValidationException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise ValidationException(f'Введите различные валюты: {base}.')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise ValidationException(f'Не удалось обработать валюту {base}')
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise ValidationException(f'Не удалось обработать валюту {quote}')
        try:
            amount = float(amount.replace(',', '.'))

            if amount <= 0:
                raise ValidationException(f'Введите сумму больше 0')
            elif amount > 1000000:
                raise ValidationException(f'Введите сумму не больше 1000000')

        except ValueError:
            raise ValidationException(f'Не удалось обработать количество {amount}')

        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        data = json.loads(response.content)

        total_base = round(data[currencies[base]], 2)
        return total_base
