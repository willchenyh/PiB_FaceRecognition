"""
What this script does:
0. assume the local host is already connected to ec2 instance
1. check if a new face image is saved in SOURCE_DIR.
3. run classification and save result txt file in RESULT_DIR.
2. change name and move the image to OLD_IMAGES_DIR.
5. send result file to DESTINATION_DIR
"""

import glob, os, subprocess

SOURCE_DIR = 'new_face' # ec2
DESTINATION_DIR = 'new_result' # pi
KEY_PAIR_PATH = 'pib_fr.pem' # 
EC2_PUBLIC_DNS = 'ec2-35-167-141-186.us-west-2.compute.amazonaws.com' # 
OLD_IMAGES_DIR = 'old_faces' # ec2
RESULT_DIR = 'new_result' # ec2

def check_new_file(path):
    new_file = None
    file_path = os.path.join(path,'*')
    file_list = glob.glob(file_path)
    if len(file_path)!=0:
        new_file = file_list[0]
    return new_file

def send_file(file_path):
    send_command = ' '.join() #TODO
    subprocess.call(send_command)
    return

def move_file(file_path):
    move_command = ' '.join('mv', file_path, OLD_IMAGE_DIR)
    subprocess.call(move_command)
    return

def present_result(result_path):
    # present result
    return

def main():
    # if a new face image is received, classify
    new_image_path = check_new_file(SOURCE_DIR)
    if new_image_path is not None:
        print 'new file present'
        send_file(new_image_path)
        move_file(new_image_path)
        # look for new result
        new_result_present = False
        while not new_result_present:
            new_result_path = check_new_file(RESULT_DIR)
            if new_result_path is not None:
                new_result_present = True
                present_result(new_result_present)
    return

if __name__ == "__main__":
    main()



