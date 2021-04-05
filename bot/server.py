from flask import Flask, session, request, redirect
import vk_api, datetime
import os
from flask_session import Session
from vk_api.audio import VkAudio
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pymongo import MongoClient
import uuid

client = MongoClient('localhost', 27017)
db = client['MUSICGEEKdb']
vk_collection = db['vk']
spotify_collection = db['spotify']

vk_oauth_config = {
    'client_id' : "7794879",
    'redirect_url_end' : "/vk_oauth_complete",
    'redirect_url_base' : "http://91.203.193.57:8000",
    'v' : "5.130",
    'basic_url_for_token' : "https://oauth.vk.com/access_token",
    'basic_url_for_code' : "https://oauth.vk.com/authorize",
    'oauth_startpoint' : "/vk_oauth",
    'grant_type' : "client_credentials",
    'client_secret' : "SsVRgiVPrle4mhxR3aOd",
    'responce_type' : "code",
    'scope' : "audio,email",
    'url' : "{basic_url_for_code}?client_id={client_id}&v={v}&redirect_uri={redirect_url_base}{redirect_url_end}&grant_type={grant_type}&client_secret={client_secret}&scope={scope}&responce_type={responce_type}&state={state}"
}


spotify_oauth_config = {
    'client_id' : "7e7a1e938e2640b6a029cf9ba3fa150b",
    'client_secret' : "c0d618591a494b34b5eb5cbba13574f6",
    'redirect_url_end' : "/spotify_oauth",
    'oauth_startpoint' : "/spotify_oauth",
    'redirect_url_base' : "http://91.203.193.57:8000",
    'scope' : "user-library-read, playlist-read-private, user-read-recently-played, user-read-playback-state, user-top-read, playlist-read-collaborative, user-read-currently-playing"
}


NAME = 'tg_id'

url2 = "{basic_url_for_token}?client_id={client_id}&redirect_uri={redirect_url_base}{redirect_url_end}&client_secret={client_secret}&code="



app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')


@app.route(vk_oauth_config['oauth_startpoint'])
def vk_oauth_start():
    tg_id = request.args.get('tg_id')
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
    return redirect(redirect_url)


@app.route(spotify_oauth_config['oauth_startpoint'])
def spotify_oauth():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())
    if request.args.get('tg_id'):
        tg_id = request.args.get('tg_id')


    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read, playlist-read-private, user-read-recently-played, user-read-playback-state, user-top-read, playlist-read-collaborative, user-read-currently-playing',
                                                cache_handler=cache_handler, 
                                                show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        tok = auth_manager.get_access_token(request.args.get("code"), as_dict = False)
        vk_collection.insert_one({
            '_id' : str(tg_id),
            'spotify_access_token' : str(tok)
        })
        print(tg_id, tok)
        try:
            # Remove the CACHE file (.cache-test) so that a new user can authorize.
            os.remove(session_cache_path())
            session.clear()
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
        return "good"

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    return "good"
        

@app.route("/start")
def start():
    return "well done"

@app.route(vk_oauth_config['redirect_url_end'])
def vk_oauth_complete():
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
    return "good"


app.run(host="0.0.0.0", port = "8000", threaded=True)
