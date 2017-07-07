
import numpy as np
from keras import optimizers
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import load_model
import keras
import cv2
import glob, os
import random

img_height, img_width, num_channel = 224, 224, 3
mean_pixel = np.array([104., 117., 123.]).reshape((1,1,3))
test_data_dir = 'data/test'
FACE = True
MNIST = False
if FACE:
    # face paths
    model_path = 'vgg16_fr_withNewFrontal_3_weights.h5'
    img_path_1 = '/home/ec2-user/Documents/PIB_FR_CNN/raw_data/will/test/16_test{}.jpg'.format('20')
    img_path_2 = '/home/ec2-user/Documents/PIB_FR_CNN/data/test/19/16_normal_{}.jpg'.format('14')
elif MNIST:
    # mnist paths
    model_path = 'vgg16_mnist_weights.h5'
    img_path_1 = '/home/ec2-user/Documents/examples/mnist/test_mnist_image.jpg'
    img_path_2 = '/home/ec2-user/Documents/examples/mnist/data/0_10.jpg'


def make_pred(img_path, model):
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
    print 'COnfidence: {} {}'.format(scores[0, sorted_idx[0, -1]], scores[0, sorted_idx[0, -2]])
    lb = np.argmax(scores)
    #print 'Predicted label:', lb
    #print keras.utils.np_utils.probas_to_classes(scores)
    return lb

# read model
model = load_model(model_path)
model.summary()
#model.compile(optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), loss='categorical_crossentropy')

# predict label for a new image
# make_pred(img_path_1, model)
def load_data(src_path):
    # under train/val/test dirs, each class is a folder with numerical numbers
    class_path_list = sorted(glob.glob(os.path.join(src_path, '*')))
    image_path_list = []
    for class_path in class_path_list:
        image_path_list += sorted(glob.glob(os.path.join(class_path, '*jpg')))
    image_counter = len(image_path_list)
    print 'This set has {} images.'.format(image_counter)

    # read images and labels
    indices = range(image_counter)
    random.shuffle(indices)
    num_selected = 40
    selected_indices = indices[:num_selected]
    #print selected_indices
    selected_paths = [image_path_list[idx] for idx in selected_indices]
    """
    X = np.zeros((num_selected, img_height, img_width, num_channel))
    Y = np.zeros((num_selected, 1))
    counter = 0
    for idx in selected:
        image_path = image_path_list[idx]
        label = int(image_path.split('/')[-2])
        image = cv2.imread(image_path, 1)
        image = cv2.resize(image, (img_height, img_width)) - mean_pixel
        #image = image.reshape((img_height, img_width, num_channel))
        X[counter, :, :, :] = image
        Y[counter, :] = label
        counter += 1
    """
    return selected_paths

"""
num_selected = 40
selected_paths = load_data(test_data_dir)
for i in range(num_selected):
    image_path = selected_paths[i]
    make_pred(image_path, model)
    label = int(image_path.split('/')[-2])
    print 'Read label:', label
"""

test_list = sorted(glob.glob('/home/ec2-user/Documents/PIB_FR_CNN/test/*jpg'))
counter = 0
for test_img in test_list:
    pred = make_pred(test_img, model)
    print '\n'
    if pred == 19:
        counter += 1
print '{} out of {} correct.'.format(counter, len(test_list))
