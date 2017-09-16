"""
What this script does:
0. this will be run in >>?
0. assume the local host is already connected to ec2 instance
1. check if a new face image is saved in IMG_SRC_DIR.
2. process and classify the image
3. save the classification result in RESULT_DIR.
4. change name and move the image to OLD_IMAGES_DIR.
"""

import glob, os, subprocess, time, cv2
import numpy as np
from keras.models import load_model

IMG_SRC_DIR = '/home/ec2-user/PiB_FaceRecognition/code_on_ec2/new_face'  # ec2
#OLD_IMAGES_DIR = '/home/ec2-user/PiB_FaceRecognition/code_on_ec2/old_faces'  # ec2
RESULT_DIR = '/home/ec2-user/PiB_FaceRecognition/code_on_ec2/new_result'  # ec2
#OLD_RESULTS_DIR = '/home/ec2-user/PiB_FaceRecognition/code_on_ec2/old_results'  # ec2
RESULT_FILE_NAME = 'result.txt'


def check_new_file(path):
    new_file_path = None
    file_path = os.path.join(path,'*')
    file_list = sorted(glob.glob(file_path))
    #print file_path
    #print file_list

    if len(file_list) != 0:
        new_file_path = file_list[0]
    return new_file_path

"""
def move_file(file_path, new_path):
    move_command = ' '.join(['mv', file_path, new_path])
    print move_command
    subprocess.call(move_command, shell=True)
    return


def classify(image_path):
    classify_command = './demos/classifier_test.py infer ./generated-embeddings/classifier.pkl ' + image_path
    print classify_command
    subprocess.call(classify_command, shell=True)
    return


def classify_test(image_path):
    result_file = open('/host/Documents/code_on_ec2/new_result/result.txt', 'w')
    result_file.write('Will,0.75')
    result_file.close()
    return
"""

def classify(file_path, model):
    img_height, img_width, num_channel = 224, 224, 3
    mean_pixel = np.array([104., 117., 123.]).reshape((1, 1, 3))
    # get image
    new_img = cv2.imread(file_path, 1)
    new_img = cv2.resize(new_img, (img_height, img_width)) - mean_pixel
    x = np.expand_dims(new_img, axis=0)
    # predict
    scores = model.predict(x, verbose=1)
    sorted_idx = np.argsort(scores)
    label = sorted_idx[0, -1]
    confidence = scores[0, sorted_idx[0, -1]]
    print 'Top 2:'
    print 'labels: {} {}'.format(label, sorted_idx[0, -2])
    print 'Confidence: {} {}'.format(confidence, scores[0, sorted_idx[0, -2]])
    #label, confidence = classify.make_pred(file_path, md)
    # write results
    result_file = open(os.path.join(RESULT_DIR, RESULT_FILE_NAME), 'w')
    if int(label) == 19:
        person = 'Will'
    else:
        person = 'Other'
    result = ','.join([person, str(confidence)])
    result_file.write(result)
    result_file.close()
    return


def main():
    # read model
    model_path = '/home/ec2-user/vgg16_new_version_weights.h5'
    model = load_model(model_path)
    model.summary()

    print 'Starting ...'
    while True:
        # check if a new face image is saved
        new_image_path = check_new_file(IMG_SRC_DIR)
        if new_image_path is not None:
            print 'New face image found!'
            new_image_path = new_image_path[0]
            # classify image
            print 'Let\'s see who you are...'
            # call the classify script and save name and confidence level in a txt file
            classify(new_image_path, model)
            print 'Now I know!'
            # clean up old
            #move_file(new_image_path, OLD_IMAGES_DIR)
            os.remove(new_image_path)
            # wait 10 seconds and move the result file to old file dir
            time.sleep(10)
            result_file_path = os.path.join(RESULT_DIR, RESULT_FILE_NAME)
            #move_file(result_file_path, OLD_RESULTS_DIR)
            os.remove(result_file_path)
        else:
            print 'Waiting for image...'
        time.sleep(1)

"""
def loop():
    print 'Starting ...'
    while True:
        main()
        time.sleep(1)
    return
"""

if __name__ == "__main__":
    main()
