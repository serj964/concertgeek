from flask import Flask, session, request

app = Flask(__name__)

client_id = "7562746"
redirect_url = "http://localhost:8000"
v = "5.130"
basic_url = "https://oauth.vk.com/authorize"
grant_type = "client_credentials"
url = basic_url+"?client_id="+client_id+"&v="+v+"&redirect_uri="+redirect_url+"&grant_type="+grant_type

@app.route('/auth')
def auth():
    tg_id = request.args.get('tg_id')
    session['key'] = tg_id
    return redirect(url)
@app.route('/auth_complete')
def auth_complete():
    tg_id = session.get('key', 'not set')
    token = request.args.get('code')
    #add this pair to db

app.run(port = 8000)