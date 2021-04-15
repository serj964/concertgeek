import telebot

TOKEN  = "1787836132:AAE6ZA6psgjHfEM5nSP9Ti5ya2AWwuIKJl8"

bot = telebot.TeleBot(TOKEN)

bot.send_message(373959637, "hey")
#bot.polling()