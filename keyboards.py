from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def full_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("RUB", callback_data="currency|RUB"),
        InlineKeyboardButton("USD", callback_data="currency|USD"),
        InlineKeyboardButton("EUR", callback_data="currency|EUR")
    )
    return markup


def keyboard_without_rub():
    markup_rub = InlineKeyboardMarkup()
    markup_rub.row_width = 2
    markup_rub.add(
        InlineKeyboardButton("USD", callback_data="currency2|USD"),
        InlineKeyboardButton("EUR", callback_data="currency2|EUR")
    )
    return markup_rub


def keyboard_without_usd():
    markup_usd = InlineKeyboardMarkup()
    markup_usd.row_width = 2
    markup_usd.add(
        InlineKeyboardButton("RUB", callback_data="currency2|RUB"),
        InlineKeyboardButton("EUR", callback_data="currency2|EUR")
    )
    return markup_usd


def keyboard_without_eur():
    markup_eur = InlineKeyboardMarkup()
    markup_eur.row_width = 2
    markup_eur.add(
        InlineKeyboardButton("RUB", callback_data="currency2|RUB"),
        InlineKeyboardButton("USD", callback_data="currency2|USD"),
    )
    return markup_eur


def greeting():
    markup_greet = InlineKeyboardMarkup()
    markup_greet.row_width = 2
    markup_greet.add(
        InlineKeyboardButton("Привет!", callback_data="hi"),
        InlineKeyboardButton("Я пойду отсюда...", callback_data="bye")
    )
    return markup_greet
