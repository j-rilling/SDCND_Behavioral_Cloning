#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 01:48:25 2019

@author: earendilavari
"""

#%% GET THE DATA FROM CSV FILE
# The training data for this project is generated by the Udacity's simulator and corresponds to three images from the front of the car
# and the corresponding turning angle for that images. The path to the images and the angle values are saved on the file driving_log.csv

import csv 
import cv2
import numpy as np

csvLines = []
with open('TrainingData1/driving_log.csv') as csvFile:
    reader = csv.reader(csvFile)
    for line in reader:
        csvLines.append(line)
        
trainingImgs = []
trainingMeasurements = []

for line in csvLines:
    imgPath = line[0]
    imgName = imgPath.split('/')[-1]
    currPath = 'TrainingData1/IMG/' + imgName
    trainingImgBGR = cv2.imread(currPath)
    trainingImgRGB = cv2.cvtColor(trainingImgBGR, cv2.COLOR_BGR2RGB)
    trainingImgs.append(trainingImgRGB)
    
    trainingMeasurement = float(line[3])
    trainingMeasurements.append(trainingMeasurement)
    
X_train = np.array(trainingImgs)
Y_train = np.array(trainingMeasurements)



#%% USING MODEL OF PROJECT 3 (TRAFFIC SIGN CLASSIFIER)
# As first model alternative for this task, the improved LeNet network used on the last project is used. Here it is programmed
# again using Keras

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout, Lambda
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPool2D


model = Sequential()
# Normalization layer (from 0-255 to 0-1)
model.add(Lambda(lambda x: x/255.0, input_shape = (160, 320, 3)))
# First convolutional layer
model.add(Conv2D(10, kernel_size=(5,5)))
model.add(Activation('relu'))
# Pooling layer
model.add(MaxPool2D(pool_size = (2,2), strides = (2,2)))
# Second convolutional layer
model.add(Conv2D(18, kernel_size=(4,4)))
model.add(Activation('relu'))
# Pooling layer
model.add(MaxPool2D(pool_size = (2,2), strides = (2,2)))
# Third convolutional layer
model.add(Conv2D(30, kernel_size=(3,3)))
model.add(Activation('relu'))
# Pooling layer
model.add(MaxPool2D(pool_size = (2,2), strides = (2,2)))
# Flatten layer
model.add(Flatten())
# First fully connected layer
model.add(Dense(490))
model.add(Dropout(0.5))
model.add(Activation('relu'))
# Second fully connected layer
model.add(Dense(220))
model.add(Dropout(0.5))
model.add(Activation('relu'))
# Third fully connected layer
model.add(Dense(43))
model.add(Activation('relu'))
# Last layer with only one output
model.add(Dense(1))

model.summary()

#%% TRAINING AND SAVING THE MODEL

model.compile(loss = 'mse', optimizer = 'adam')
model.fit(X_train, Y_train, validation_split=0.2, shuffle = True)
model.save('model.h5')


























 