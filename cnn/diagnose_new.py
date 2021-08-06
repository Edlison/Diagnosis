# -*- coding: utf-8 -*-
"""diagnose_new.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vW0mbXJ6Q5RybZ5gFSH3_FfGzoNjwiZy
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import *
from PIL import Image

#input
    # model_path: the pre-trained model
    # file_path: the image you want to upload
#output
    # 1, have cancer
    # 0, healthy
    # -1, wrong size
    # -2, not image
def diagnose_with_model(img):
    img = Image.open(img)

    # load the model
    model_path = 'cnn/data/Model_now'
    model = tf.keras.models.load_model(model_path)
    
    # check the image size
    if (img.size[0]!=50 or img.size[1]!=50):
        return -1
    
    # preprocessing
    img = image.img_to_array(img)
    img /= 255.0
    
    # predict it with the cnn model
    y_prob = model.predict(img.reshape(-1,50,50,3))

    # return the classified result 0/1
    return np.argmax(y_prob)


if __name__ == '__main__':
    ...
