from flask import Flask, session, request, redirect
import vk_api, datetime
from flask_session import Session

client_id = "7562746"


redirect_url_end = "/auth_complete"
redirect_url_base = "http://localhost:8000"
v = "5.130"
basic_url_for_token = "https://oauth.vk.com/access_token" #for access_token
basic_url_for_code = "https://oauth.vk.com/authorize" #for code
grant_type = "client_credentials"
client_secret = "rqozJXDcBPrygXS181xr"
responce_type = "code"
scope = "audio,email"


NAME = 'tg_id'

url = basic_url_for_code+"?client_id="+client_id+"&v="+v+"&redirect_uri="+redirect_url_base+redirect_url_end+"&grant_type="+grant_type+"&client_secret="+client_secret+"&scope="+scope+"&responce_type="+responce_type
url2 = basic_url_for_token+"?client_id="+client_id+"&redirect_uri="+redirect_url_base+redirect_url_end+"&client_secret="+client_secret+"&code="


@app.route('/auth')
def auth():
    tg_id = request.args.get('tg_id')
    print(tg_id)
    session[NAME] = tg_id
    return redirect(url)
@app.route(redirect_url_end)
def auth_complete():
    tg_id = session.get(NAME, 'not set')
    session.pop(NAME, default=None)
    code = request.args.get('code')
    vk_session = vk_api.VkApi(app_id=client_id, client_secret=client_secret, scope = '8')

    try:
        vk_session.code_auth(code, redirect_url_base+redirect_url_end)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    

    email = vk_session.token['email']
        
    vk_session = vk_api.VkApi(login = vk_session.token['email'], token = vk_session.token['access_token'])

    try:
        vk_session.auth(token_only = True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return



    print(tg_id, email)
    #add this pair to db
    #if code:
    #    return redirect(url2+code)
    #else:
    #    email = request.args.get('email')
    #    access_token = request.args.get('access_token')
    #    print(email, access_token)
    return "good"


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.run(port = 8000)