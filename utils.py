
# coding: utf-8

# In[55]:


import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt


# In[59]:


IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)


# In[81]:


def read_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return np.array(img)


# In[42]:


def resize_image(img):
    new_img = cv2.resize( img, (IMAGE_WIDTH,IMAGE_HEIGHT) )
    return new_img


# In[61]:


def crop_image(img):
    new_img = img[60:-25,:,:]
    return new_img


# In[62]:


def process_img(path):
    img = read_image(path)
    img = crop_image(img)
    img = resize_image(img)
    return img

def process(image):
    img = crop_image(image)
    img = resize_image(img)
    return img

# In[185]:


def choose_image(path_row, steering):
    ch = np.random.choice(3)
    img = process_img( path_row[ch] )
    steering_angle = float(steering)

    #for left
    if (ch == 1):
        steering_angle += 0.2
    #for right
    if (ch == 2):
        steering_angle -= 0.2
    
    return img, steering_angle


# In[183]:


def flip_image(img, angle):
    ch = np.random.choice(2)
    if ch == 0:
        return img, angle
    else:
        return cv2.flip(img,1), -angle


# In[203]:


def generate_dataset():
    
    df = pd.read_csv('driving_log.csv')
    X = df[['center','left','right']].values
    Y = df['steering'].values
    
    data_X = np.empty( [X.shape[0], IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS ], dtype='uint8' )
    data_Y = np.empty( [ Y.shape[0] ] )
    for i in range(X.shape[0]):

        img, angle = choose_image(X[i], Y[i])
        img, angle = flip_image(img, angle)

        data_X[i] = img
        data_Y[i] = angle
        
    return data_X, data_Y

