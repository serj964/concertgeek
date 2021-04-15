import telebot
import datetime
TOKEN = "1713650415:AAHpmqcTLVPFaoOtTi_POHk6Z66j3tr3ac4"

bot = telebot.TeleBot(TOKEN)
CHAT_ID = -560631730


LOGS_PATH = "/home/testServer/musicGEEK/logs/"
DBO_FNAME = "db.o"
DBE_FNAME = "db.e"
BOTO_FNAME = "bot.o"
BOTE_FNAME = "bot.e"
SERVERO_FNAME = "server.o"
SERVERE_FNAME = "server.e"




#dbo_fd = open(LOGS_PATH+DBO_FNAME,"r")
#dbe_fd = open(LOGS_PATH+DBE_FNAME,"r")
boto_fd = open(LOGS_PATH+BOTO_FNAME,"r")
#bote_fd = open(LOGS_PATH+BOTE_FNAME,"r")
#servero_fd = open(LOGS_PATH+SERVERO_FNAME,"r")
#servere_fd = open(LOGS_PATH+SERVERE_FNAME,"r")





while True:
    boto_line = boto_fd.readline()
    if boto_line != "":
        current_time = datetime.datetime.now()
        bot.send_message(CHAT_ID, "[BOT OUTPUT - "+boto_line.split()[0]+"]")
        #bot.send_message(CHAT_ID, boto_line)