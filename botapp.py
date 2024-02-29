import telebot

from config import TOKEN
from Extentions import CryptoConverter, ValidationException
from Currencies import currencies

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    text = f'Добро пожаловать @{message.chat.username} в чат для конвертации валют!\n' \
           'Для начала работы введите команду в следующем формате (через пробел):' \
           ' \n- Название валюты, цену которой Вы хотите узнать  \n- Название валюты, в которой Вы хотите узнать ' \
           'цену первой валюты \n- Количество первой валюты\n' \
           'Нажмите /currencies, чтобы увидеть список доступных валют\n' \
           'Если вдруг Вам нужна помощь, нажмите /help'

    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = 'Нажмите /currencies, чтобы увидеть список доступных валют \n' \
           'Для начала работы введите команду в следующем формате (через пробел):' \
           ' \n- Название валюты, цену которой Вы хотите узнать  \n- Название валюты, в которой Вы хотите узнать ' \
           'цену первой валюты \n- Количество первой валюты\n' \
           'Для того, чтобы начать нашу беседу сначала, нажмите /start'

    bot.reply_to(message, text)


@bot.message_handler(commands=['currencies'])
def command_currencies(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.title().split()

        if len(values) != 3:
            raise ValidationException('Неверно введены параметры. \n'
                                      'Введите еще раз валюты и количество первой валюты\n'
                                      'Пример: Доллар Евро 100\n'
                                      'Нажмите /help, если у Вас есть затруднения')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except ValidationException as e:
        bot.reply_to(message, f'Ошибка пользователя{e}\n')
        bot.register_next_step_handler(message, get_price)

    except Exception as e:
        bot.reply_to(message, f'Что-то пошла не так! Ошибка\n{e}\n'
                              'Нажмите /help, если у Вас есть затруднения')
        bot.register_next_step_handler(message, get_price)
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)
        bot.reply_to(message, f'@{message.chat.username}, чтобы продолжить, повторите ввод данных')
        bot.register_next_step_handler(message, get_price)


bot.polling(none_stop=True)