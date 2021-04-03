from flask import Flask, session, request, redirect
import vk_api, datetime
from flask_session import Session
#from Music_analyzer.vk_music_analyzer import vk_music_analyzer
from vk_api.audio import VkAudio
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['MUSICGEEKdb']

vk_collection = db['vk']
spotify_collection = db['spotify']

vk_oauth_config = {
    'client_id' : "7794879",
    'redirect_url_end' : "/auth_complete",
    'redirect_url_base' : "http://91.203.193.57",
    'v' : "5.130",
    'basic_url_for_token' : "https://oauth.vk.com/access_token",
    'basic_url_for_code' : "https://oauth.vk.com/authorize",
    'grant_type' : "client_credentials",
    'client_secret' : "SsVRgiVPrle4mhxR3aOd",
    'responce_type' : "code",
    'scope' : "audio,email",
    'url' : "{basic_url_for_code}?client_id={client_id}&v={v}&redirect_uri={redirect_url_base}{redirect_url_end}&grant_type={grant_type}&client_secret={client_secret}&scope={scope}&responce_type={responce_type}&state={state}"
}


spotify_oauth_config = {
    'client_id' : "7e7a1e938e2640b6a029cf9ba3fa150b",
    'client_secret' : "c0d618591a494b34b5eb5cbba13574f6",
    'redirect_url_end' : "/spotify",
    'redirect_url_base' : "http://91.203.193.57:7000",
    'scope' : "user-library-read, playlist-read-private, user-read-recently-played, user-read-playback-state, user-top-read, playlist-read-collaborative, user-read-currently-playing"
}


NAME = 'tg_id'

url2 = "{basic_url_for_token}?client_id={client_id}&redirect_uri={redirect_url_base}{redirect_url_end}&client_secret={client_secret}&code="

app = Flask(__name__)










@app.route('/auth')
def auth():
    tg_id = request.args.get('tg_id')
    auth_scope = request.args.get('scope')
    if auth_scope == "vk": #vk
        redirect_url = vk_oauth_config['url'].format(
                                                basic_url_for_code = vk_oauth_config['basic_url_for_code'],
                                                client_id = vk_oauth_config['client_id'],
                                                v = vk_oauth_config['v'],
                                                redirect_url_base = vk_oauth_config['redirect_url_base'],
                                                redirect_url_end = vk_oauth_config['redirect_url_end'],
                                                grant_type = vk_oauth_config['grant_type'],
                                                client_secret = vk_oauth_config['client_secret'],
                                                scope = vk_oauth_config['scope'],
                                                responce_type = vk_oauth_config['responce_type'],
                                                state = tg_id)
        print(redirect_url)
        return redirect(redirect_url)



    elif auth_scope == "spotify": #spotify
        auth_manager = SpotifyOAuth(client_id=spotify_oauth_config['client_id'],
                                               client_secret=spotify_oauth_config['client_secret'],
                                               redirect_uri=spotify_oauth_config['redirect_url_base']+spotify_oauth_config['redirect_url_end'],
                                               scope=spotify_oauth_config['scope'], open_browser = True)

        
        #sp = spotipy.Spotify(auth_manager = auth_manager)
        #spotify_id = sp.current_user()['id']

        token = auth_manager.get_access_token()['access_token']
        spotify_collection.insert_one({
            '_id' : str(tg_id),
            'spotify_access_token' : token
        })
        #error process
        #print(tg_id, spotify_id)
        return "good"
        

@app.route(vk_oauth_config['redirect_url_end'])
def auth_complete():
    tg_id = request.args.get('state')
    code = request.args.get('code') 
    vk_session = vk_api.VkApi(app_id=vk_oauth_config['client_id'], client_secret=vk_oauth_config['client_secret'], scope = '8')

    try:
        vk_session.code_auth(code, vk_oauth_config['redirect_url_base']+vk_oauth_config['redirect_url_end'])
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    

    vk = vk_session.get_api()
    resp = vk.users.get(v=5.89, name_case="Nom")
    vk_id = resp[0]['id']
    vk_collection.insert_one({
            '_id' : str(tg_id),
            'vk_id' : str(vk_id)
        })
    print(tg_id, vk_id)

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
