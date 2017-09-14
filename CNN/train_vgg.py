"""
ECE196 Face Recognition Project
Author: W Chen

Use this as a template to:
1. load weights for vgg16
2. load images
3. finetune network
4. save weights
"""

from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras import optimizers
from keras.layers import Dropout, Flatten, Dense
from keras.utils.np_utils import to_categorical
import numpy as np
import glob
import os
import cv2
import random

IMG_H, IMG_W, NUM_CHANNELS = 224, 224, 3
MEAN_PIXEL = np.array([104., 117., 123.]).reshape((1,1,3))
TRAIN_DIR = '../data/train'
VAL_DIR = '../data/validation'
NUM_EPOCHS = 10
BATCH_SIZE = 16
NUM_CLASSES = 20
TASK_NAME = 'fr_withNewFrontal_3'


def load_model():
    # build the VGG16 network
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(IMG_H, IMG_W, NUM_CHANNELS))
    print('Model weights loaded.')
    base_out = base_model.output
    flat = Flatten()(base_out)
    hidden = Dense(256, activation='relu')(flat)
    drop = Dropout(0.5)(hidden)
    predictions = Dense(NUM_CLASSES, activation='softmax')(drop)
    model = Model(inputs=base_model.input, outputs=predictions)
    print 'Build model'

    # compile the model
    model.compile(optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print 'Compile model'
    return model


def process_image(image):
    # zero pad 5-pixel boundary
    temp = np.zeros((IMG_H+10, IMG_W+10, NUM_CHANNELS))
    temp[5:IMG_H+5, 5:IMG_H+5, :] = image
    # random horizontal flip
    flip = np.asarray(range(2))
    flip_choice = np.random.choice(flip)
    if flip_choice == 1:
        temp = cv2.flip(temp, 1)
    # random cropping
    crop = np.asarray(range(10))
    crop_choice = np.random.choice(crop, 2, False)  # starting pixel location
    row, col = crop_choice[0], crop_choice[1]
    new_image = temp[row:row+IMG_H, col:col+IMG_W, :]
    return new_image


def load_data(src_path):
    # under train/val/test dirs, each class is a folder with numerical numbers
    class_path_list = sorted(glob.glob(os.path.join(src_path, '*')))
    image_path_list = []
    for class_path in class_path_list:
        image_path_list += sorted(glob.glob(os.path.join(class_path, '*jpg')))
    random.shuffle(image_path_list)
    num_images = len(image_path_list)
    print '-- This set has {} images.'.format(num_images)
    X = np.zeros((num_images, IMG_H, IMG_W, NUM_CHANNELS))
    Y = np.zeros((num_images, 1))
    # read images and labels
    for i in range(num_images):
        image_path = image_path_list[i]
        label = int(image_path.split('/')[-2])
        image = cv2.imread(image_path, 1)
        #image = process_image(image)
        image = cv2.resize(image, (IMG_H, IMG_W)) - MEAN_PIXEL
        #image = image.reshape((IMG_H, IMG_W, NUM_CHANNELS))
        #image -= MEAN_PIXEL
        X[i, :, :, :] = image
        Y[i, :] = label
    Y = to_categorical(Y, NUM_CLASSES)
    return X, Y


def main():
    # make model
    model = load_model()
    print 'VGG16 created\n'
    # Get data
    print 'Load train data:'
    X_train, Y_train = load_data(TRAIN_DIR)
    print 'Load val data:'
    X_val, Y_val = load_data(VAL_DIR)
    # Train model
    model.fit(X_train, Y_train, batch_size=BATCH_SIZE, epochs=5, validation_data=(X_val, Y_val))
    print '\n'
    # Save model weights
    model.save('vgg16_{}_weights.h5'.format(TASK_NAME))
    print 'model weights saved.'
    return


if __name__ == '__main__':
    main()
