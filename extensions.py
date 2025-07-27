import requests
import json


class APIException(Exception):
    """Пользовательское исключение для ошибок при обработке запросов."""
    pass


class CurrencyConverter:
    """Класс для конвертации валют через CryptoCompare API."""

    # Словарь соответствия русских названий и кодов валют
    CURRENCY_CODES = {
        'евро': 'EUR',
        'доллар': 'USD',
        'рубль': 'RUB',
        'eur': 'EUR',
        'usd': 'USD',
        'rub': 'RUB'
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        """
        Возвращает цену на указанное количество валюты.

        :param base: Валюта для конвертации (например, 'евро')
        :param quote: Валюта, в которую конвертируем (например, 'рубль')
        :param amount: Количество конвертируемой валюты
        :return: Сумма в целевой валюте
        """
        # Приводим введённые названия к нижнему регистру
        base = base.lower()
        quote = quote.lower()

        # Проверяем и преобразуем валюты
        base_code = CurrencyConverter.CURRENCY_CODES.get(base)
        quote_code = CurrencyConverter.CURRENCY_CODES.get(quote)

        if not base_code:
            raise APIException(f"Валюта '{base}' не поддерживается.")
        if not quote_code:
            raise APIException(f"Валюта '{quote}' не поддерживается.")

        # Проверяем корректность количества
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            raise APIException("Количество должно быть положительным числом.")

        # Формируем и отправляем запрос к API
        url = f"https://min-api.cryptocompare.com/data/price?fsym={base_code}&tsyms={quote_code}"
        response = requests.get(url)
        data = json.loads(response.text)

        # Обработка возможных ошибок API
        if response.status_code != 200:
            raise APIException("Ошибка подключения к серверу курсов валют.")

        if 'Response' in data and data['Response'] == 'Error':
            raise APIException(f"Ошибка API: {data.get('Message', 'Неизвестная ошибка')}")

        if quote_code not in data:
            raise APIException("Не удалось получить курс для указанных валют.")

        # Рассчитываем результат
        rate = data[quote_code]
        result = rate * amount
        return round(result, 2)