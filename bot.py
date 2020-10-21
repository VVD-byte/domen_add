# -*- coding: utf8 -*-
import telebot
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from telebot import TeleBot, types
import threading
import re
import copy
from bs4 import BeautifulSoup
import json
import datetime

bot = TeleBot('1343297949:AAE-SzfEhgJNQANYVTN5FrJIJl126Z3lumk')

class pars:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--log-level=3')
        self.options.headless = True
        self.buy = {}
        self.binary = FirefoxBinary('/opt/firefox/firefox')
        
    def start(self, text):
        try:
            self.buy = {}
            for i in text:
                self.buy[i] = 'Поиск начался'
                x = threading.Thread(target = self.start_1, args=(i,))
                x.start()
        except:
            pass

    def start_1(self, i):
        try:
            dr = webdriver.Firefox(firefox_options = self.options, executable_path = './geckodriver', firefox_binary = self.binary)
            #dr = webdriver.Firefox(firefox_options = self.options, executable_path = 'geckodriver.exe')
            self.buy[i] = 'Подмена Cookies'
            dr.get('https://ca.auctions.godaddy.com/')
            with open("cookies.json", "r") as t:
                data = json.loads(t.read())
            dr.delete_all_cookies()
            for cookie in data:
                dr.add_cookie(cookie)
            self.buy[i] = 'Поиск домена'
            dr.find_element_by_css_selector('input[id*="txtKeywordContext"').send_keys(i)
            time.sleep(30)
            dr.find_element_by_css_selector('button[class*="btn btn-primary"').click()
            time.sleep(20) #############3
            soup = BeautifulSoup(dr.page_source, 'lxml')
            try:
                idd = soup.find_all('span',{'title':'View details for %s'%i})[0].find_all('img')[0]['id'].split('_')[1]
                dr.get('https://ca.auctions.godaddy.com/trpItemListing.aspx?miid=%s'%idd)
            except:
                self.buy[i] = 'Домен не найден'
            time.sleep(25)##############place_bid    addToCart
            if self.wait(i, dr):
                self.buy_dom(i, dr)
        except:
            self.buy[i] = 'ERROR AUTH'
    
    def wait(self, i, dr):
        try:
            if 'src="https://img1.wsimg.com/domain-auctions/static/4dd4b62/img/hammer-icon-grayed-out.svg"' in dr.page_source or 'id="addToCart"' in dr.page_source:
                self.buy[i] = 'Домен найден, ожидание'
                return True
            else:
                self.buy[i] = 'Bid домена не равен 0'
                dr.close()
                return False
        except:
            self.buy[i] = 'ERROR WAIT'

    def buy_dom(self, i, dr):
        global bot
        while 1:
            try:
                dr.find_element_by_css_selector('button[id*="addToCart"').click() ###############################
                self.buy[i] = 'Домен зарезервирован'
                bot.send_message(362896381, i + ' Домен зарезервирован', reply_markup = markup)
                time.sleep(10)
                dr.close()
            except:
                pass

a = pars()


markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
itembtn1 = types.KeyboardButton('Ввести домены')
itembtn2 = types.KeyboardButton('Получить прогресс')
markup.row(itembtn1, itembtn2)

def us(funk):
    def wrap(message, *args, **kwargs):
        if message.chat.id == 271411622 or message.chat.id == 362896381:
            funk(message)
    return wrap

@bot.message_handler(commands = ['start'])
@us
def start(message):
    bot.send_message(message.chat.id, "Привет", reply_markup = markup)

@bot.message_handler(regexp = "Ввести домены")
@us
def start_domen(message):
    bot.send_message(message.chat.id, "Введи все домены через перенос строки", reply_markup = markup)

@bot.message_handler(regexp = "Получить прогресс")
@us
def process(message):
    try:
        text = ''
        for i in a.buy:
            text += i + ' - ' + a.buy[i] + '\n'
        bot.send_message(message.chat.id, text, reply_markup = markup)
    except:
        bot.send_message(message.chat.id, "На данный момент домены не отслеживаются", reply_markup = markup)

@bot.message_handler(regexp = r'')
@us
def d(message):
    text = message.text.replace(' ', '').split('\n')
    text_q = [str(idd+1) + '. ' + i for idd, i in enumerate(text)]
    bot.send_message(message.chat.id, '\n'.join(text_q), reply_markup = markup)
    bot.send_message(message.chat.id, 'Скрипт запущен', reply_markup = markup)
    x = threading.Thread(target = a.start, args=(text,))
    x.start()

bot.infinity_polling(True)


#173.212.227.166:3452
#gdsniper
##$%@#EFW3243ds