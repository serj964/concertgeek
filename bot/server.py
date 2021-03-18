from flask import Flask, session, request, redirect
import vk_api, datetime
from flask_session import Session
#from Music_analyzer.vk_music_analyzer import vk_music_analyzer
from vk_api.audio import VkAudio


client_id = "7794879"


redirect_url_end = "/auth_complete"
redirect_url_base = "http://localhost:8000"
v = "5.130"
basic_url_for_token = "https://oauth.vk.com/access_token" #for access_token
basic_url_for_code = "https://oauth.vk.com/authorize" #for code
grant_type = "client_credentials"
client_secret = "SsVRgiVPrle4mhxR3aOd"
responce_type = "code"
scope = "audio,email"


NAME = 'tg_id'

url = basic_url_for_code+"?client_id="+client_id+"&v="+v+"&redirect_uri="+redirect_url_base+redirect_url_end+"&grant_type="+grant_type+"&client_secret="+client_secret+"&scope="+scope+"&responce_type="+responce_type
url2 = basic_url_for_token+"?client_id="+client_id+"&redirect_uri="+redirect_url_base+redirect_url_end+"&client_secret="+client_secret+"&code="

app = Flask(__name__)


@app.route('/auth')
def auth():
    tg_id = request.args.get('tg_id')
    return redirect(url)
@app.route(redirect_url_end)
def auth_complete():
    #tg_id = request.args.get('state')
    code = request.args.get('code') 
    vk_session = vk_api.VkApi(app_id=client_id, client_secret=client_secret, scope = '8')

    try:
        vk_session.code_auth(code, redirect_url_base+redirect_url_end)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    

    vk = vk_session.get_api()
    resp = vk.users.get(v=5.89, name_case="Nom")
    print(resp)

    #vk = vk_music_analyzer()
    #print(email)
    #print(vk.get_favourite_artists(vk_session))
    #add this pair to db
    #if code:
    #    return redirect(url2+code)
    #else:
    #    email = request.args.get('email')
    #    access_token = request.args.get('access_token')
    #    print(email, access_token)
    return "good"


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.run(port = 8000)
