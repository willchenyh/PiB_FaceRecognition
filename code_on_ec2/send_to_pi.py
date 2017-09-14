"""
What this script does:
0. this will be run in >>?
0. assume the local host is already connected to ec2 instance
1. check if a new face image is saved in IMG_SRC_DIR.
2. process and classify the image
3. save the classification result in RESULT_DIR.
4. change name and move the image to OLD_IMAGES_DIR.
"""

import glob, os, subprocess, time
import classify
from keras.models import load_model

IMG_SRC_DIR = '/home/ec2-user/Documents/code_on_ec2/new_face'  # ec2
OLD_IMAGES_DIR = '/home/ec2-user/Documents/code_on_ec2/old_faces'  # ec2
RESULT_DIR = '/home/ec2-user/Documents/code_on_ec2/new_result'  # ec2
OLD_RESULTS_DIR = '/home/ec2-user/Documents/code_on_ec2/old_results'  # ec2
RESULT_FILE_NAME = 'result.txt'

# read model
model_path = '/home/ec2-user/Documents/vgg16_new_version_weights.h5'
model = load_model(model_path)
model.summary()


def check_new_file(path, num_files):
    new_file_path = None
    file_path = os.path.join(path,'*')
    file_list = sorted(glob.glob(file_path))
    #print file_path
    #print file_list
    num_files = int(num_files)
    if len(file_list) == num_files:
        new_file_path = file_list[0:num_files]
    return new_file_path


def move_file(file_path, new_path):
    move_command = ' '.join(['mv', file_path, new_path])
    print move_command
    subprocess.call(move_command, shell=True)
    return

'''
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
'''

def classify_keras(file_path, md):
    label, confidence = classify.make_pred(file_path, md)
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
    # check if a new face image is saved
    new_image_path = check_new_file(IMG_SRC_DIR, 1)
    if new_image_path is not None:
        print 'New face image found!'
        new_image_path = new_image_path[0]
        # classify image
        print 'Let\'s see who you are...'
        # call the classify script and save name and confidence level in a txt file
        classify_keras(new_image_path, model)
        print 'Now I know!'
        # clean up old
        move_file(new_image_path, OLD_IMAGES_DIR)
        # wait 10 seconds and move the result file to old file dir
        time.sleep(10)
        result_file_path = os.path.join(RESULT_DIR, RESULT_FILE_NAME)
        move_file(result_file_path, OLD_RESULTS_DIR)
        print 'Moved files to old dir'
    else:
        print 'Waiting for image...'
    return


def loop():
    print 'Starting ...'
    while True:
        main()
        time.sleep(1)
    return


if __name__ == "__main__":
    loop()



