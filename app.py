from flask import Flask, render_template, request, session
from flask.ext.socketio import SocketIO, emit, send, disconnect

from stream_twitter import *


application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(application)

@application.route('/')
def index():
    return "hello stream"

@application.route('/stream')
def stream_render():
    return render_template('stream.html') 

@socketio.on('connect', namespace='/test')
def test_connect():
    print('connected')
    emit('response', {'data': 'Connected!', 'count': 0})

def tweet_callback(message):
    print('broadcasting message={}'.format(message))
    socketio.emit('response', {'data': message}, namespace='/test')

@socketio.on('my event', namespace='/test')
def test_message(message):
    print('Event coming!')
    emit('response', {'data': message['data']})
    ListenerAction(auth, 1, tweet_callback)

@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('response', {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()
    socketio.run(application, debug=True)
