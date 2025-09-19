from flask_socketio import SocketIO

class MessageEmitter:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio

    def emit(self, message):
        self.socketio.emit('server_response', message)