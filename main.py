import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from math import radians, cos, sin, asin, sqrt


FILENAME = "map.csv"
API_TOKEN = ':'
bot = telebot.TeleBot(API_TOKEN)
totalmap_string="Mappa completa delle vedovelle"
def leggidati(file_name):
    
    dati = []

    try:
        fountains_file = open(FILENAME,"r",encoding="utf-8")
    except:
        print("errore file csv")

    next(fountains_file) #salto la prima riga
    for line in fountains_file:
        line=line.strip().split(";")
        value=[]

        lng=float(line[5])
        value.append(lng)
        lat=float(line[6])
        value.append(lat)
        name=str(line[4])
        value.append(name)

        dati.append(value)

    return dati

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Manda La tua posizione', request_location=True)
    itembtn2 = types.KeyboardButton(totalmap_string)
    markup.add(itembtn1,itembtn2)
    bot.send_message(message.chat.id, """Le fontanelle nel capoluogo lombardo (in totale sono 668) hanno una lunga storia e una tradizione interessante, tanto da poter vantare ben due soprannomi. 
    Il primo è quello di “vedovelle”, che deriva dal getto d’acqua continuo, paragonabile a quello di una donna in lutto che piange per la propria perdita. 
    E poi c’è la dicitura di “drago verde”, un nome che unisce il caratteristico colore della struttura – un verde ramarro – e la bocca in ghisa a forma di drago (ma ne esistono anche con altri animali).\
""" ,reply_markup=markup)
    bot.send_photo(message.chat.id, 'https://static.wikia.nocookie.net/milano/images/6/61/Vedovella.jpg/revision/latest/scale-to-width-down/1200?cb=20171020121313&path-prefix=it')
    bot.reply_to(message, """\
Ciao, per favore mandami la tua posizione per trovare la vedovella più vicina📍\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if (message.text)!=totalmap_string:
        bot.reply_to(message,"""Non riesco a capire, per favore mandami la tua posizione per trovare la vedovella più vicina📍\
""")
    else:
        sendlinkmap(message)
 
 #in questo modo mando la posizione tramite send_location e per ricavare le latitudini e longitudine utilizzo il campo 'location' e lat o lng ecc...
 #la parte importante è la prima riga in cui devo specificicare il content_types=["location"]
@bot.message_handler(content_types=["location"])
def location_received(message):
    bot.send_message(message.chat.id,"Posizione ricevuta")    
    searchnearfountains(message.location.latitude, message.location.longitude,message)

def searchnearfountains(lat_current,lng_current,message):
    dati=leggidati(FILENAME)
    rmb=mindistancefountains(dati,lat_current,lng_current)
    lng_result=dati[rmb][0]
    lat_result=dati[rmb][1]
    name_result=dati[rmb][2]
    bot.send_location(message.chat.id,  lat_result , lng_result)
    bot.send_message(message.chat.id,"Ecco la vedovella più vicina :)")
    bot.send_message(message.chat.id,"Distanza: "+str(round(distance(lat_current,lng_current,lat_result,lng_result))) + "m")
    bot.send_message(message.chat.id,name_result)

def mindistancefountains(dati,lat_current,lng_current):
    minima_distance=pow(pow(lat_current - dati[0][1], 2) + pow(lng_current - dati[0][0], 2), .5)
    countrmb=0
    for value in dati:
        distance=pow(pow(lat_current - value[1], 2) + pow(lng_current - value[0], 2), .5)
        if(distance<minima_distance):
            minima_distance=distance
            rmb=countrmb
        countrmb=countrmb+1
    return rmb

def distance(lat1,lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return((c * r)*1000)

def sendlinkmap(message):
    bot.send_message(message.chat.id, "Ecco qua⬇️", reply_markup=gen_markup())

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Mappa", url='https://www.fontanelle.org/Mappa-Fontanelle-Milano-Lombardia.aspx'),)
    return markup


bot.infinity_polling()
