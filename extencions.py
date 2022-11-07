import requests
import json
from config import exchanges

class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return  ApiException(message, f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ApiException(message, f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise ApiException(message, f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ApiException(message, f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        return round(new_price, 2)
