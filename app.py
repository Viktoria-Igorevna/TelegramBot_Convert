import telebot
from confing import keys, TOKEN
from extensions import APIException, CryptoConverter
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = f'Привет, {message.chat.username}! Этот бот умеет конвертировать валюты.\n\n\
Как писать командy - /help\n\
Чтобы увидеть все валюты - /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Для перевода введите команду в следующем формате:\n<валюта>\
<в какую валюту перевести>\
<количество переводимой валюты>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Не верное количество параметров')

        quote, base, amount = values
        rez = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {keys[quote]} = {rez} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()