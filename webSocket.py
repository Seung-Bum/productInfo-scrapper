from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)


def send_message(message):  # 웹 소켓으로 메시지 전송
    socketio.emit('update', {'data': message})


def long_running_task():  # 작업을 수행하는 함수
    for i in range(1, 11):
        time.sleep(1)  # 가상의 작업을 시뮬레이션하기 위해 1초 동안 대기
        send_message(f'Task in progress: {i}/10')

    send_message('Task completed!')


@app.route('/')  # 홈페이지 렌더링
def index():
    return render_template('home.html')


@socketio.on('connect')  # 웹 소켓 이벤트 핸들러
def handle_connect():
    send_message('Connected to the server.')


# 시작 지점
if __name__ == '__main__':
    # 백그라운드 스레드에서 작업 실행
    task_thread = Thread(target=long_running_task)
    task_thread.start()

    # Flask 웹 애플리케이션 실행
    socketio.run(app, debug=True)
