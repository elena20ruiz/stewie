from server.spotify import calls as sp_calls
from flask import Flask, request, redirect, g, render_template, session


app = Flask(__name__)
app.secret_key = 'some key for session'

# ----------------------- AUTH API PROCEDURE -------------------------

@app.route("/auth")
def auth():
    return redirect(sp_calls.AUTH_URL)



@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    auth_header = sp_calls.authorize(auth_token)
    session['auth_header'] = auth_header
    print('HI:' + auth_header)

def valid_token(resp):
    return resp is not None and not 'error' in resp

# -------------------------- API REQUESTS ----------------------------

@app.route("/")
def index():
    return render_template('template/index.html')

if __name__ == '__main__':
    app.run(debug=True, port=sp_calls.PORT)