# musicGEEK
service for melomans
#run bot (root derictory of the project):
python3 -m bot.music_geek_bot.py
python3 -m bot.server.py
#run db:
docker-compose up -d
#make migration:
yoyo apply migrations.sql
#stop db:
docker stop MUSICGEEK_db
#remove db:
docker rm MUSICGEEK_db
