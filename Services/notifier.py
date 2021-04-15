import sqlalchemy
import telebot
import time



#connect with db

TOKEN = "1787836132:AAE6ZA6psgjHfEM5nSP9Ti5ya2AWwuIKJl8"
TIMETICK = 60


bot = telebot.TeleBot(TOKEN)

def Notify():
    #check db and if there are some events, it will notify user
    bot.send_message(373959637, "hey")

while True:
    Notify()
    time.sleep(TIMETICK)