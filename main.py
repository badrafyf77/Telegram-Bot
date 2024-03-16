import telebot
from telegram_text import PlainText
from decouple import config
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import time

def escape_text(text):
    element = PlainText(text)
    escaped_text = element.to_markdown()
    return escaped_text

def send_message(image_url, title, descreption, coupon, category, price, language):
    try:
        image = requests.get(image_url)
        message_content = f"""
🟣 Title: *{escape_text(title)}*
{escape_text(descreption)}

ℹ️ *Additional informations*
>🔶 You will receive a certificate when you pass the course
>🏷️ Price: *~{escape_text(price)}~*  🆓FREE
>📚 Category: {escape_text('#' + category)}
>🌐 Course Language: {escape_text(language)}
[Click here to take the course]({coupon})

EverythingToKnow✅
"""
        bot.send_photo(CHANNEL_ID, photo=image.content, caption=message_content, parse_mode='MarkdownV2')
    except:
        print("error")


def check_coupon(coupon):
    return coupon not in my_coupons

my_coupons = []

def get_text(coupon_list, title_list, description_list, image_list,categories_list, prices_list, languages_list):
    for (title, description, image_url, category, price, language, coupon) in zip(title_list, description_list, image_list, categories_list, prices_list, languages_list, coupon_list):
        if(check_coupon(coupon)):
            my_coupons.append(coupon)
            print('coupon number : ' + str(len(my_coupons)))
            send_message(image_url, title, description, coupon, category, price, language)



def get_coupons(go_links):
    coupons = []
    titles = []
    descriptions = []
    for coupon_link in go_links:
        res = requests.get(coupon_link)
        soup = BeautifulSoup(res.text, 'html.parser')
        coupon = soup.find('div', attrs={'class': 'ui segment'}).a['href']
        title = soup.find('h1', attrs={'class': 'ui grey header'}).getText()
        description = soup.find('div', attrs={'class': 'ui attached segment'}).p.getText()
        coupons.append(coupon)
        titles.append(title)
        descriptions.append(description)
    return get_text(coupons, titles, descriptions, images,categories, prices, languages)

categories = []
prices = []
languages = []
images = []
def get_go_links(list_url):
    go_link = []
    for link in list_url:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        link_class = soup.find('div', attrs={'class': 'ui center aligned basic segment'}).a['href']
        src_attribute = soup.find('amp-img', class_='ui centered bordered image').get('src')
        category_name = soup.find('div', class_='ui small breadcrumb').find('a').text.strip()
        price_span = soup.find('span', class_='price').text.strip()
        language_span = soup.find('span', class_='languages').text.strip()
        go_link.append(link_class)
        images.append(src_attribute)
        categories.append(category_name)
        prices.append(price_span)
        languages.append(language_span)
    return get_coupons(go_link)


def get_links(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    link_class = soup.select('.card-header')
    hn = []
    for idx, item in enumerate(link_class):
        href = link_class[idx].get('href')
        hn.append(href)
    return get_go_links(hn)


def process():
    try:
        try:
            get_links('https://www.discudemy.com/all')
        except ConnectionError:
            print('[!] Please check your network connection!')
    except KeyboardInterrupt:
        print('[!] CTRL + C detected\n[!] Quitting...')


def main():
    while True:
        process()
        time.sleep(180)



BOT_TOKEN = config('BOT_TOKEN')
CHANNEL_ID = config('CHANNEL_ID')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message): 
    main()

bot.polling()