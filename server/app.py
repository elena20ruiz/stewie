from server.spotify import calls as sp_calls
from server.spotify import parse as sp_parse
from flask import Flask, request, redirect, g, render_template, session, jsonify
import server.model_state.domain_controller as dc
import pprint

app = Flask(__name__)
app.secret_key = 'some key for session'

domainController = None

# ----------------------- AUTH API PROCEDURE -------------------------

@app.route("/auth")
def auth():
    return redirect(sp_calls.AUTH_URL)

@app.route("/connect", methods=["GET"])
def connect():
    # GET PLAYLIST
    res_playlist = sp_calls.get_current_playlist(session['auth_header'])
    id_playlist = sp_parse.get_current_playlist_from_info(res_playlist)
    print('PLAYLIST:' + id_playlist)
    # STORE SONGS
    res_songs = sp_calls.get_tracks_from_playlist_call(id_playlist, session['auth_header'])
    res_info_songs = sp_parse.get_info_tracks(res_songs, session['auth_header'])

    domainController = dc.DomainController()
    domainController.getEmotionPredictionModel()
    domainController.computePlaylistEmotionPrediction(id_playlist)

    return jsonify(res_info_songs)

    # GET DEVICE TO CONNECT
    #res = sp_calls.get_available_devices(session['auth_header'])
    #id_device = sp_parse.get_id_of_tablet(res)
    # CONNECT TO DEVICE
    #if id_device:
    #    res = sp_calls.connect_to_device(session['auth_header'],id_device)
    #    return jsonify(id_playlist)
    #else:
    #    return jsonify({'NO PLAYING'})
    # CONNECT
    # CALL MODEL TRAINING
    # REORDER LIST


@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    auth_header = sp_calls.authorize(auth_token)
    session['auth_header'] = auth_header
    return jsonify(auth_header)

# -------------------------- API REQUESTS ----------------------------

@app.route("/")
def index():
    return render_template('template/index.html')

if __name__ == '__main__':
    app.run(debug=True, port=sp_calls.PORT)