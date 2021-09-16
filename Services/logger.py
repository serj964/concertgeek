import telebot
import datetime
import json

TOKEN = "1713650415:AAHpmqcTLVPFaoOtTi_POHk6Z66j3tr3ac4"

bot = telebot.TeleBot(TOKEN)
CHAT_ID = -560631730

CONFIG_FILE = './bot/config.json'

with open(CONFIG_FILE) as conf:
    config = json.load(conf)

LOGS_PATH = config["logs_config"]
DBO_FNAME = "db.o"
DBE_FNAME = "db.e"
BOTO_FNAME = "bot.o"
BOTE_FNAME = "bot.e"
SERVERO_FNAME = "server.o"
SERVERE_FNAME = "server.e"




#dbo_fd = open(LOGS_PATH+DBO_FNAME,"r")
#dbe_fd = open(LOGS_PATH+DBE_FNAME,"r")
#bote_fd = open(LOGS_PATH+BOTE_FNAME,"r")
#servero_fd = open(LOGS_PATH+SERVERO_FNAME,"r")
#servere_fd = open(LOGS_PATH+SERVERE_FNAME,"r")


LOGFILE = LOGS_PATH+"log.log"
with open(LOGFILE, "a") as f, open(LOGS_PATH+BOTO_FNAME,"r") as boto_fd:
    while True:
        boto_line = boto_fd.readline()
        if boto_line != "":
            current_time = datetime.datetime.now()
            log_string = "[BOT OUTPUT - "+current_time.strftime("%d/%m/%Y %H:%M:%S")+" - "+boto_line.split()[0]+"]: "+' '.join(boto_line.split()[1:])
            f.write(log_string+"\n")
            f.flush()
            bot.send_message(CHAT_ID, log_string)
            #bot.send_message(CHAT_ID, boto_line)