"""
What this script does:
0. this will be run in openface root directory in docker
0. assume the local host is already connected to ec2 instance
1. check if a new face image is saved in IMG_SRC_DIR.
2. process and classify the image
3. save the classification result in RESULT_DIR.
4. change name and move the image to OLD_IMAGES_DIR.
"""

import glob, os, subprocess, time

IMG_SRC_DIR = '/host/Documents/code_on_ec2/new_face'  # ec2
OLD_IMAGES_DIR = '/host/Documents/code_on_ec2/old_faces'  # ec2
RESULT_DIR = '/host/Documents/code_on_ec2/new_result'  # ec2
OLD_RESULTS_DIR = '/host/Documents/code_on_ec2/old_results'  # ec2
RESULT_FILE_NAME = 'result.txt'


def check_new_file(path, num_files):
    new_file = None
    file_path = os.path.join(path,'*')
    file_list = glob.glob(file_path)
    #print file_path
    #print file_list
    num_files = int(num_files)
    if len(file_list) == num_files:
        new_file = file_list[0:num_files]
    return new_file


def move_file(file_path, new_path):
    move_command = ' '.join(['mv', file_path, new_path])
    print move_command
    subprocess.call(move_command, shell=True)
    return


def classify(image_path):
    subprocess.call('./demos/classifier_test.py infer ./generated-embeddings/classifier.pkl '+image_path, shell=True)
    return


def main():
    # check if a new face image is saved
    new_image_path = check_new_file(IMG_SRC_DIR, 1)
    if new_image_path is not None:
        print 'New face image found!'
        new_image_path = new_image_path[0]
        # classify image
        print 'Let\'s see who you are...'
        # TODO: call the classify script and save name and confidence level in a txt file
        classify(new_image_path)
        # clean up old
        move_file(new_image_path, OLD_IMAGES_DIR)
        # wait 10 seconds and move the result file to old file dir
        time.sleep(10)
        result_file_path = os.path.join(RESULT_DIR, RESULT_FILE_NAME)
        move_file(result_file_path, OLD_RESULTS_DIR)
    return


if __name__ == "__main__":
    main()



