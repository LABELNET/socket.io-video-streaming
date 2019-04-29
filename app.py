#!/usr/bin/env python
from importlib import import_module
import os
import socketio

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# socket
sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connection established')


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


# @sio.on('domebar/live', namespace='/ops')
# def on_domebar(msg):
#     print(msg)


def gen(camera):
    while True:
        frame = camera.get_frame()
        sio.emit('domebar/live', frame)


if __name__ == '__main__':
    # Camera
    camera = Camera()
    sio.connect('http://192.168.0.103:7001', namespaces=['/ops'])
    sio.emit('domebar/live', 'ops live', namespace='/ops')
    while True:
        frame = camera.get_frame()
        sio.emit('domebar/live', frame,namespace='/ops')
