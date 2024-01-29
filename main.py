import telebot
from telebot import types 
import markups
import requests
import json
import io
bot = telebot.TeleBot("6754978495:AAGbx8Q8JrKxc4ENkBkC2f6Y8Ya-gTXtTf0")

@bot.message_handler(commands= ["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(markups.welcomeMenu[0], markups.welcomeMenu[1])
    markup.add(markups.welcomeMenu[2], markups.welcomeMenu[3])
    bot.send_message(message.from_user.id, text="Здравствуйте!", reply_markup=markup)
    
    f = open('taobaoresponse.json')
    data = json.load(f)
   
    f.close()

    
@bot.message_handler(content_types=['text'])
def WelcomeMenu(message):
    if (message.text == "Поиск товаров 🔍"):
        shop = types.ReplyKeyboardMarkup(resize_keyboard=True)
        shop.add(markups.searchItems[0], markups.searchItems[1])
        shop.add(markups.searchItems[2], markups.searchItems[3])
        bot.send_message(message.from_user.id, text="Выберите магазин", reply_markup=shop)
    if (message.text == "Taobao"):
        bot.send_message(message.chat.id, "Что вы хотите купить?")
        bot.register_next_step_handler(message, requestTaobao)



def requestTaobao(message):
    url = "https://api.taobao-scraping-api.com/taobao/searchItem"

    querystring = { "q": f"{message.text}", "pageNum":"1"}

    headers = {
        "Content-Type": "application/json",
        "APIKey": "k_6792c08d5d84bb6fd9bb6f21cc0e4bf4"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    inlineMarkup.add(detail_urlbtn)
    for i in data["items"]["item"]:
        print(i["title"])
        title = i["title"]
        original_price = i["price"]
        pic_url = i["pic_url"]
        detail_url = i["detail_url"]
        inlineMarkup = types.InlineKeyboardMarkup()
        detail_urlbtn = types.InlineKeyboardButton("Детальная информация", url=detail_url)
        inlineMarkup.pop()
        bot.send_photo(message.chat.id, photo=pic_url, caption=f"{title} \n Цена: {original_price}, \n Детальная информация: {detail_url}", reply_markup=inlineMarkup)
        bot.edit_message_reply_markup(None)
    return data
    

bot.polling(none_stop=True, interval=0)