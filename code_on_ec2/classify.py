
import numpy as np
from keras.models import load_model
import cv2
import glob, os
import random

img_height, img_width, num_channel = 224, 224, 3
mean_pixel = np.array([104., 117., 123.]).reshape((1,1,3))
test_data_dir = 'data/test'
# face paths
model_path = 'vgg16_fr_withNewFrontal_3_weights.h5'
#img_path_1 = '/home/ec2-user/Documents/PIB_FR_CNN/raw_data/will/test/16_test{}.jpg'.format('20')
#img_path_2 = '/home/ec2-user/Documents/PIB_FR_CNN/data/test/19/16_normal_{}.jpg'.format('14')
# read model
model = load_model(model_path)
model.summary()
#model.compile(optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), loss='categorical_crossentropy')


def make_pred(img_path):
    # predict label for a new image
    print img_path
    new_img = cv2.imread(img_path, 1)
    new_img = cv2.resize(new_img, (img_height, img_width)) - mean_pixel
    #print type(new_img), new_img.shape
    # new_img = image.load_img(img_path_2, target_size=(img_height, img_width, num_channel))
    #x = image.img_to_array(new_img)
    x = np.expand_dims(new_img, axis=0)
    #print type(x), x.shape
    # x = preprocess_input(x)
    scores = model.predict(x, verbose=1)
    #print 'Load image successfully'
    #print scores
    sorted_idx = np.argsort(scores)
    print 'Top 2 labels: {} {}'.format(sorted_idx[0, -1], sorted_idx[0, -2])
    print 'Confidence: {} {}'.format(scores[0, sorted_idx[0, -1]], scores[0, sorted_idx[0, -2]])
    lb = sorted_idx[0, -1]
    conf = scores[0, sorted_idx[0, -1]]
    #print 'Predicted label:', lb
    #print keras.utils.np_utils.probas_to_classes(scores)
    return lb, conf


