import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    """Отправляет инструкции по использованию бота."""
    instructions = (
        " Конвертер валют\n\n"
        " Формат запроса:\n"
        "<валюта1> <валюта2> <количество>\n\n"
        "Примеры:\n"
        " евро рубль 100\n"
        " доллар евро 50\n"
        " рубль доллар 5000\n\n"
        "Доступные команды:\n"
        "/values - список доступных валют\n"
        "/help - инструкции"
    )
    bot.reply_to(message, instructions)


@bot.message_handler(commands=['values'])
def send_currencies(message):
    """Отправляет список доступных валют."""
    currencies = (
        " Доступные валюты:\n"
        " Евро (евро, eur)\n"
        " Доллар США (доллар, usd)\n"
        " Российский рубль (рубль, rub)"
    )
    bot.reply_to(message, currencies)


@bot.message_handler(content_types=['text'])
def convert_currency(message):
    """Обрабатывает запрос на конвертацию валют."""
    try:
        # Разбиваем сообщение на части
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException(
                "Неверный формат запроса.\nИспользуйте: <валюта1> <валюта2> <количество>\nПример: евро рубль 100")

        base, quote, amount = parts
        result = CurrencyConverter.get_price(base, quote, amount)

        # Форматируем вывод
        response = (
            f" {amount} {base.upper()} = {result} {quote.upper()}\n"
            f"1 {base.upper()} = {result / float(amount):.4f} {quote.upper()}"
        )
        bot.reply_to(message, response)

    except APIException as e:
        bot.reply_to(message, f" Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"️ Неизвестная ошибка: {e}")


if __name__ == "__main__":
    bot.polling(none_stop=True)