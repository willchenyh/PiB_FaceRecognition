"""
What this script does:
0. assume the local host is already connected to ec2 instance
1. check if a new face image is saved in IMG_SRC_DIR.
2. send image to ec2 instance's IMG_DEST_DIR.
3. change name and move the image to OLD_IMAGES_DIR.
4. check if a new result is saved in RESULT_DEST_DIR.
5. read and present result
"""

import glob, os, subprocess, time

EC2_IP = "ec2-user@ec2-52-25-37-56.us-west-2.compute.amazonaws.com"  # ec2 TODO
KEY_PAIR_PATH = "/home/pi/PiB_FaceRecognition/code_on_pi/aws_personal.pem"  # local TODO

IMG_SRC_DIR = '/home/pi/PiB_FaceRecognition/code_on_pi/new_face'  # local
IMG_DEST_DIR = '/home/ec2-user/PiB_FaceRecognition/code_on_ec2/new_face'  # ec2

#OLD_IMAGES_DIR = '/home/pi/PiB_FaceRecognition/code_on_pi/old_faces'  # local
RESULT_SRC_DIR = "/home/ec2-user/PiB_FaceRecognition/code_on_ec2/new_result/result.txt"  # ec2
RESULT_DEST_DIR = "/home/pi/PiB_FaceRecognition/code_on_pi/new_result"  # local
#OLD_RESULTS_DIR = '/home/pi/PiB_FaceRecognition/code_on_pi/old_results'  # local


def check_new_file(path):
    new_file_path = None
    file_path = os.path.join(path,'*')
    file_list = sorted(glob.glob(file_path))
    
    #print file_path
    #print file_list

    if len(file_list) ==1:
        new_file_path = file_list[0]
    return new_file_path


def send_file(file_path):
    send_command = ' '.join(['scp', '-i', KEY_PAIR_PATH, file_path, EC2_IP+':'+IMG_DEST_DIR])
    #print send_command
    subprocess.call(send_command, shell=True)
    print 'sending file to server'
    return

"""
def move_file(in_file_path, out_file_path):
    move_command = ' '.join(['mv', in_file_path, out_file_path])
    print move_command
    subprocess.call(move_command, shell=True)
    return
"""

def fetch_file():
    fetch_command = ["scp", "-i", KEY_PAIR_PATH, EC2_IP+":"+RESULT_SRC_DIR, RESULT_DEST_DIR]
    #print fetch_command
    while True:
        try:
            subprocess.check_call(fetch_command)
            return
        except subprocess.CalledProcessError:
            continue

"""
def extract_result_file(result_list):
    result_path = result_list[0]
    #if result_path[-1] == 'r':
    #    result_path = result_list[1]
    return result_path
"""

def present_result(result_path):
    # present result
    result_file = open(result_path, 'r')
    result = result_file.read()
    details = result.split(',')
    name = details[0]
    conf = details[1]
    print name, conf
    return name, conf


def main():

    # check if a new face image is saved on pi
    new_image_path = check_new_file(IMG_SRC_DIR)

    if new_image_path is not None:
        # send it to ec2, and archive it
        #new_image_path = new_image_path[0]
        send_file(new_image_path)
        #shutil.move(new_image_path, OLD_IMAGES_DIR)
        os.remove(new_image_path)
        print 'Let\'s see who you are...'
        # look for new result
        new_result_present = False
        while not new_result_present:
            for i in range(3):
                time.sleep(1)
                print 'Still thinking...'
            fetch_file()
            new_result_path = check_new_file(RESULT_DEST_DIR)
            #print new_result_list
            if new_result_path is not None:
                print 'New result found!'
                #new_result_present = True
                #new_result_path = extract_result_file(new_result_list)
                """
                move_file(new_result_path, OLD_RESULTS_DIR)
                """
                return present_result(new_result_path)

            else:
                print 'Still thinking...'
    #return

"""
def loop():
    print 'Starting ...'
    while True:
        main()
        time.sleep(1)
    return
"""
