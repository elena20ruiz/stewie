from server.spotify import calls as sp_calls
from server.spotify import parse as sp_parse
from flask import Flask, request, redirect, g, render_template, session, jsonify
import server.model_state.domain_controller as dc
import pprint

app = Flask(__name__)
app.secret_key = 'some key for session'

main_playlist = ''
# ----------------------- AUTH API PROCEDURE -------------------------

@app.route("/auth")
def auth():
    return redirect(sp_calls.AUTH_URL)

@app.route("/connect", methods=["GET"])
def connect():
    # GET PLAYLIST
    res_playlist = sp_calls.get_current_playlist(session['auth_header'])
    id_playlist = sp_parse.get_current_playlist_from_info(res_playlist)
    main_playlist = id_playlist
    print('PLAYLIST:' + id_playlist)
    # STORE SONGS
    domainController.setToken(session['auth_header'])
    domainController.getEmotionPredictionModel()
    domainController.computePlaylistEmotionPrediction(id_playlist)
    return id_playlist

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


@app.route("/list_playlist")
def list_playlist():
    list_tracks = domainController.processImage()
    res_playlist = sp_calls.get_current_playlist(session['auth_header'])
    id_playlist = sp_parse.get_current_playlist_from_info(res_playlist)
    sp_calls.reorder_playlist(id_playlist, list_tracks, session['auth_header'])
    song = sp_calls.get_current_track(session['auth_header'])
    response = {
        'name': song['item']['name'],
        'artist': song['item']['album']['artists'][0]['name']
    }
    return jsonify(response)

@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    auth_header = sp_calls.authorize(auth_token)
    session['auth_header'] = auth_header
    return jsonify(auth_header)


@app.route("/pausesong", methods=["GET"])
def pausesong():
    domainController.pauseSong()
    return "OK"

@app.route("/playsong", methods=["GET"])
def playsong():
    domainController.playSong()
    return "OK"

@app.route("/nextsong", methods=["GET"])
def nextsong():
    domainController.nextSong()
    return "OK"

# -------------------------- API REQUESTS ----------------------------

@app.route("/")
def index():
    return render_template('template/index.html')

if __name__ == '__main__':
    domainController = dc.DomainController()
    app.run(debug=True, host="0.0.0.0",port=sp_calls.PORT)
