import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import base64
from datetime import datetime
import shutil
import numpy as np
import socketio 
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
import utils
from keras.models import load_model
import argparse

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str,
                    help='Enter IP address for socket', default = '0.0.0.0')
parser.add_argument('--min_speed', type=int,
                    help='Enter Minimum Speed of Car', default = 10)
parser.add_argument('--max_speed', type=int,
                    help='Enter Maximum Speed of Car', default = 25)
parser.add_argument('--path', type=str,
                    help='Enter path to saved model file', default = './model.h5')


args = parser.parse_args()

path = args.path
ip = args.ip
MAX_SPEED = args.max_speed
MIN_SPEED = args.min_speed
speed_limit = MAX_SPEED

model = load_model(path)


sio = socketio.Server()
app = Flask(__name__)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)

@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])
        #print (steering_angle, throttle, speed)
        
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        
        try:
            image = np.asarray(image)       
            image = utils.process(image) 
            image = image/255.0
            image = np.array([image])       
            
            steering_angle = float(model.predict(image, batch_size=1))

            global speed_limit
            if speed > speed_limit:
                speed_limit = MIN_SPEED  # slow down
            else:
                speed_limit = MAX_SPEED
                
            throttle = 1.0 - ( (steering_angle)**2 ) - ( (speed/speed_limit)**2 )
            #throttle = 1.0
            
            print('{} {} {}'.format(steering_angle, throttle, speed))
            send_control(steering_angle, throttle)
            
        except Exception as e:
            print(e)
        
    else:
        sio.emit('manual', data={}, skip_sid=True)
    


app = socketio.Middleware(sio, app)
eventlet.wsgi.server(eventlet.listen((ip, 4567)), app)

