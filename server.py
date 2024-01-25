from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


def background_thread():
    for i in range(1, 11):
        # 1초마다 클라이언트에 현재 카운트 값을 전송
        socketio.emit('update_count', i)
        time.sleep(1)


if __name__ == '__main__':
    # 백그라운드 스레드 시작
    thread = threading.Thread(target=background_thread)
    thread.daemon = False
    thread.start()

    # 소켓IO 서버 실행
    socketio.run(app, debug=True)
