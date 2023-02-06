import telebot
import json

token = ''

bot = telebot.TeleBot(token, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    with open('2_items_things.json') as file:
        templat = json.load(file)
    things = [*templat.values()]
    for i in things:
        result = f'\n{i["item_name"]} \n\nЦена со скидкой: {i["item_price"]} \nЦена без скидки: ~{i["item_oldprice"]}~'
        bot.send_media_group(message.chat.id, media=[telebot.types.InputMediaPhoto(open('msxrctwe_nb_02_i.webp', 'rb'), caption=result, parse_mode='MarkdownV2'),
                                           telebot.types.InputMediaPhoto(open('msxrctwe_nb_03_i.webp', 'rb'))],)


bot.infinity_polling()



