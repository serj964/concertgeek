# concertgeek
service for melomans (copy of main from 01/09/21)
## run bot (root derictory of the project):
python3 -m bot.music_geek_bot.py
python3 -m bot.server.py
## run db (db directory):
docker-compose up -d \
if port is already used: sudo ss -lptn 'sport = :5432' and then sudo kill
## make migration (db directory):
yoyo apply migrations.sql
## stop db (db directory):
docker stop MUSICGEEK_db
## remove db (db directory):
docker rm MUSICGEEK_db
