
# coding: utf-8

# In[4]:

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import base64
from datetime import datetime
import os
import shutil
import numpy as np
import socketio 
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO

from keras.models import load_model

import utils


# In[5]:


model = load_model('./model.h5')


# In[6]:


sio = socketio.Server()
app = Flask(__name__)
MAX_SPEED = 25
MIN_SPEED = 10
speed_limit = MAX_SPEED

# In[7]:


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)


# In[8]:


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
    

# In[9]:


app = socketio.Middleware(sio, app)
eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 4567)), app)

