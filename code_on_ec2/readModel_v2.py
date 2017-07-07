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

test_data_dir = 'data/test'
img_width, img_height, num_channel = 224, 224, 3
mean_pixel = np.array([104., 117., 123.]).reshape((1,1,3))
num_epochs = 5
batch_size = 16
num_classes = 20
task_name = 'fr'
model_path = 'vgg16_fr_withNewFrontal_3_weights.h5'


def load_data(src_path):
    # under train/val/test dirs, each class is a folder with numerical numbers
    class_path_list = sorted(glob.glob(os.path.join(src_path, '*')))
    image_path_list = []
    for class_path in class_path_list:
        image_path_list += sorted(glob.glob(os.path.join(class_path, '*jpg')))
    image_counter = len(image_path_list)
    print 'This set has {} images.'.format(image_counter)
    X = np.zeros((image_counter, img_height, img_width, num_channel))
    Y = np.zeros((image_counter, 1))
    # read images and labels
    for i in range(image_counter):
        image_path = image_path_list[i]
        label = int(image_path.split('/')[-2])
        image = cv2.imread(image_path, 1)
        image = cv2.resize(image, (img_height, img_width)) - mean_pixel
        #image = image.reshape((img_height, img_width, num_channel))
        X[i, :, :, :] = image
        Y[i, :] = label
    Y = to_categorical(Y, num_classes)
    return X, Y


def main():
    # load model
    model = load_model(model_path)
    model.summary()
    #model.compile(optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), loss='categorical_crossentropy')
    # Get test accuracy
    print 'Load test data:'
    X_test, Y_test = load_data(test_data_dir)
    score = model.evaluate(X_test, Y_test, batch_size)
    print model.metrics_names
    print score
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    return


if __name__ == '__main__':
    main()


