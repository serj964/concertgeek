import telebot
TOKEN = "1713650415:AAHpmqcTLVPFaoOtTi_POHk6Z66j3tr3ac4"

bot = telebot.TeleBot(TOKEN)
CHAT_ID = -560631730

FILENAME = "log.fifo"

fd = open(FILENAME,"r")




while True:
    line = fd.readline()
    if line != "":
        bot.send_message(CHAT_ID, line)git