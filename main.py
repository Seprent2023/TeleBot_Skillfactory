import sys
import telebot
import keyboards
from extensions import CurrencyConvertor, ConvertionException, variables
from config import exchange, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    text = "Что бы начать работу наберите /start или нажмите на гиперссылку.\n" \
           "Для дальнейшей работы просто нажимайте на нужные кнопки на экране и " \
           "укажите сумму для конвертации когда это потребуется.\n" \
           "Для просмотра всех возможных для конвертации валют, наберите /exc или нажмите на гиперссылку"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет {message.chat.first_name}, это коневертировщик валюты",
                     reply_markup=keyboards.greeting())


@bot.message_handler(commands=['exc'])
def start(message: telebot.types.Message):
    text = f"У этого боты вам доступен калькулятор для конвертации следующей валюты: "
    for key in exchange.keys():
        text = '\n'.join((text, key,))
    text += "\nДля начала работы наберите /start или нажмите на гиперссылку."
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def any_text(message: telebot.types.Message):
    text = "Что бы начать работу наберите /start\nДля вызова меню помощи /help"
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def first_currency(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Пожалуйста укажите валюту КОТОРУЮ вы хотите коневертировать',
                     reply_markup=keyboards.full_keyboard())


@bot.message_handler(func=lambda message: True)
def second_currency(message: telebot.types.Message):
    chat_id = message.chat.id
    if message.text == 'И Рубли превращаются...':
        bot.send_message(chat_id, 'Пожалуйста укажите валюту В КОТОРУЮ вы хотите коневертировать',
                         reply_markup=keyboards.keyboard_without_rub())
    elif message.text == 'И Доллары превращаются...':
        bot.send_message(chat_id, 'Пожалуйста укажите валюту В КОТОРУЮ вы хотите коневертировать',
                         reply_markup=keyboards.keyboard_without_usd())
    elif message.text == 'И Евро превращаются...':
        bot.send_message(chat_id, 'Пожалуйста укажите валюту В КОТОРУЮ вы хотите коневертировать',
                         reply_markup=keyboards.keyboard_without_eur())


@bot.callback_query_handler(func=lambda call: True)
def answer_for_greetin(call):
    if 'hi' in call.data:
        msg = bot.send_message(call.message.chat.id, "Приступим")
        first_currency(msg)
    if 'bye' in call.data:
        bot.send_message(call.message.chat.id, "Ну не очень то и хотелось...")
        sys.exit(0)
    else:
        answer(call)


@bot.callback_query_handler(func=lambda call: call)
def answer(call):
    if "currency|" in call.data:
        value = call.data.split("|")[1]
        chat_id = call.message.chat.id
        variables.append(value)
        if value == "RUB":
            bot.send_message(chat_id, "Вы выбрали Рубли")
            msg = bot.send_message(chat_id, "И Рубли превращаются...")
            second_currency(msg)
        elif value == "USD":
            bot.send_message(chat_id, "Вы выбрали Доллары")
            msg = bot.send_message(chat_id, "И Доллары превращаются...")
            second_currency(msg)
        elif value == "EUR":
            bot.send_message(chat_id, "Вы выбрали Евро")
            msg = bot.send_message(chat_id, "И Евро превращаются...")
            second_currency(msg)
    if 'currency2|' in call.data:
        chat_id = call.message.chat.id
        value = call.data.split("|")[1]
        variables.append(value)
        if value == "RUB":
            bot.send_message(chat_id, "в Рубли!")
            msg2 = bot.send_message(chat_id, "Какую сумму будем конвертировать?")
            bot.register_next_step_handler(msg2, quantity)
        elif value == "USD":
            bot.send_message(chat_id, "в Доллары!")
            msg2 = bot.send_message(chat_id, "Какую сумму будем конвертировать?")
            bot.register_next_step_handler(msg2, quantity)
        elif value == "EUR":
            bot.send_message(chat_id, "в Евро!")
            msg2 = bot.send_message(chat_id, "Какую сумму будем конвертировать?")
            bot.register_next_step_handler(msg2, quantity)


@bot.message_handler(func=lambda message: True)
def quantity(message: telebot.types.Message):
    try:
        digit = message.text
        if not digit.isdigit():
            raise ConvertionException(f"Не удалось обработаться {digit}, нужно вводить только целые числа.\n"
                                      f"Повторите набор в правильном формате")
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
        bot.register_next_step_handler(message, quantity)
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду {e}, наверное что-то пошло не так...")
    else:
        variables.append(int(digit))
        results(message)


def results(message):
    texts = CurrencyConvertor.get_price()
    bot.send_message(message.chat.id, f"За {variables[2]} {variables[0]}, дают {round(texts, 2)} {variables[1]}")


if __name__ == '__main__':
    bot.infinity_polling()
