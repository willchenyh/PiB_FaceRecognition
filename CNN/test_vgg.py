"""
ECE196 Face Recognition Project
Author: W Chen

Use this as a template to:
1. load saved weights for vgg16
2. load test set
3. compute accuracy for test set
"""

import numpy as np
from keras.models import load_model
import keras
import cv2
import glob, os
from keras.models import Model
from keras import applications
from keras import optimizers
from keras.utils.np_utils import to_categorical
import glob
import os

TEST_DIR = 'data/test'
MODEL_PATH = 'vgg16_fr_withNewFrontal_3_weights.h5'
IMG_H, IMG_W, NUM_CHANNELS = 224, 224, 3
MEAN_PIXEL = np.array([104., 117., 123.]).reshape((1,1,3))
NUM_EPOCHS = 10
BATCH_SIZE = 16
NUM_CLASSES = 20


def load_data(src_path):
    # under train/val/test dirs, each class is a folder with numerical numbers
    class_path_list = sorted(glob.glob(os.path.join(src_path, '*')))
    image_path_list = []
    for class_path in class_path_list:
        image_path_list += sorted(glob.glob(os.path.join(class_path, '*jpg')))
    num_images = len(image_path_list)
    print '-- This set has {} images.'.format(num_images)
    X = np.zeros((num_images, IMG_H, IMG_W, NUM_CHANNELS))
    Y = np.zeros((num_images, 1))
    # read images and labels
    for i in range(num_images):
        image_path = image_path_list[i]
        label = int(image_path.split('/')[-2])
        image = cv2.imread(image_path, 1)
        image = cv2.resize(image, (IMG_H, IMG_W)) - MEAN_PIXEL
        X[i, :, :, :] = image
        Y[i, :] = label
    Y = to_categorical(Y, NUM_CLASSES)
    return X, Y


def main():
    # load model
    model = load_model(MODEL_PATH)
    model.summary()

    # compute test accuracy
    print 'Load test data:'
    X_test, Y_test = load_data(TEST_DIR)
    score = model.evaluate(X_test, Y_test, BATCH_SIZE)
    print model.metrics_names
    print score
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    return


if __name__ == '__main__':
    main()