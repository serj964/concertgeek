from flask import Flask, session, request, redirect

app = Flask(__name__)

client_id = "7562746"
redirect_url = "http://localhost:8000/auth_complete"
v = "5.130"
#basic_url = "https://oauth.vk.com/access_token" #for access_token
basic_url = "https://oauth.vk.com/authorize" #for code
grant_type = "client_credentials"
client_secret = "rqozJXDcBPrygXS181xr"
scope="audio"
url = basic_url+"?client_id="+client_id+"&v="+v+"&redirect_uri="+redirect_url+"&grant_type="+grant_type+"&client_secret="+client_secret+"&scope="+scope

@app.route('/auth')
def auth():
    tg_id = request.args.get('tg_id')
    session['key'] = tg_id
    return redirect(url)
@app.route('/auth_complete')
def auth_complete():
    tg_id = session.get('key', 'not set')#not set?
    token = request.args.get('code')
    print(tg_id, token)
    #add this pair to db
    
    return "good"


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.run(port = 8000)