
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
        
X_train = []
Y_train = []

for line in csvLines:
    correctionFactor = 0.2
    for i in range(3):
        imgPath = line[i]
        imgName = imgPath.split('/')[-1]
        currPath = 'TrainingData1/IMG/' + imgName
        trainingImgBGR = cv2.imread(currPath)
        trainingImgRGB = cv2.cvtColor(trainingImgBGR, cv2.COLOR_BGR2RGB)
        trainingFlippedImgRGB = cv2.flip(trainingImgRGB, 1)
        X_train.append(trainingImgRGB)
        X_train.append(trainingFlippedImgRGB)
        if i == 0:
            trainingMeasurement = float(line[3])
        elif i == 1:
            trainingMeasurement = float(line[3]) + correctionFactor
        elif i == 2:
            trainingMeasurement = float(line[3]) - correctionFactor
        Y_train.append(trainingMeasurement)
        Y_train.append(-trainingMeasurement)

        
X_train = np.array(X_train)
Y_train = np.array(Y_train)



#%% DEFINITION OF THE MODEL

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
os.environ['QT_STYLE_OVERRIDE']='gtk2'

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

from keras.callbacks import Callback

class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.trainingLoss = []

    def on_batch_end(self, batch, logs={}):
        self.trainingLoss.append(logs.get('loss'))

model.compile(loss = 'mse', optimizer = 'adam')
datalogBatches = LossHistory()
datalogEpochs = model.fit(X_train, Y_train, validation_split=0.2, shuffle = True, epochs = 20, callbacks = [datalogBatches])
model.save('model.h5')

#%% SAVES DATA TO BE ANALYSED AFTERWARDS

import pickle
with open('modelDatalog.p', 'wb') as pickleFile:
    pickle.dump(datalogBatches.trainingLoss, pickleFile)
    pickle.dump(datalogEpochs.history['loss'], pickleFile)
    pickle.dump(datalogEpochs.history['val_loss'], pickleFile)





















 