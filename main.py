
import os
import telebot
from bm25 import *  

API_KEY = '5864100242:AAHBb-XyBXU-AgaOO9sNk9bx6Jsjwg-kUFA'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start','change_language'])
def hello(message):
    bot.send_message(message.chat.id, 'Choose Language:\n\n English -> /en \n हिन्दी (Hindi) -> /hi \n తెలుగు (Telugu) -> /te \n தமிழ் (Tamil) -> /ta \n മലയാളം (Malayalam) -> /ml \n ಕನ್ನಡ (Kannada) -> /kn \n বাংলা (Bengali) -> /bn \n ગુજરાતી (Gujarati) -> /gu \n मराठी (Marathi) -> /mr \n ଓଡ଼ିଆ (Odia) -> /or \n ਪੰਜਾਬੀ (Punjabi) -> /pa \n اردو (Urdu) -> /ur \n ')

@bot.message_handler(commands=['en'])
def en(message):
    try:
        LANG = 'en'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")
     
            
@bot.message_handler(commands=['hi'])
def en(message):
    try:
        LANG = 'hi'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['te'])
def en(message):
    try:
        LANG = 'te'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['ta'])
def en(message):
    try:
        LANG = 'ta'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['ml'])
def en(message):
    try:
        LANG = 'ml'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['kn'])
def en(message):
    try:
        LANG = 'kn'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['bn'])
def en(message):
    try:
        LANG = 'bn'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['gu'])
def en(message):
    try:
        LANG = 'gu'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['mr'])
def en(message):
    try:
        LANG = 'mr'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")

@bot.message_handler(commands=['or'])
def en(message):
    try:
        LANG = 'or'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")       

@bot.message_handler(commands=['pa'])
def en(message):
    try:
        LANG = 'or'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")       

@bot.message_handler(commands=['ur'])
def en(message):
    try:
        LANG = 'ur'
        config = configparser.ConfigParser()
        config.read('variables.ini')
        config.set('VARIABLES', 'LANG',str(LANG))

        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        q='Hi, welcome to Covid-19 chatbot\nAsk any question related to Covid-19 in textbox\nTo change the language of chatbot type '
        q=translation(q,LANG)
        rep=q+' /change_language'
        bot.send_message(message.chat.id,  rep)
    except:
        bot.send_message(message.chat.id,"Unable change Language")     


@bot.message_handler(commands=['more_details'])
def det(message):
    try:
        ds=more_details()
        bot.send_message(message.chat.id, ds)
    except:
        bot.send_message(message.chat.id,  'Unexpexted Error')

@bot.message_handler(func=lambda m: True)
def send_txt(message):
    try:
        query = message.text
        res=result(str(query))
        bot.send_message(message.chat.id, res)
        config = configparser.ConfigParser()
        config.read('variables.ini')
        LANG=config['VARIABLES']['LANG']
        BOOL=config['VARIABLES']['BOOL']
        LANG=LANG.replace('"','')
        if int(BOOL)==1:
            q='For more details -> '
            q=translation(q,LANG)
            rep = q+' /more_details'
            bot.send_message(message.chat.id,  rep)

    except:
        bot.send_message(message.chat.id,  'Unexpexted Error')

bot.polling()