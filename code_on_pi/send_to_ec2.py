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

EC2_IP = 'ec2-user@ec2-35-167-141-186.us-west-2.compute.amazonaws.com'  # ec2 TODO
IMG_SRC_DIR = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/new_face'  # local
IMG_DEST_DIR = '/home/ec2-user/Documents/code_on_ec2/new_face'  # ec2
KEY_PAIR_PATH = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/pib_fr.pem'  # local
OLD_IMAGES_DIR = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/old_faces'  # local
RESULT_SRC_DIR = '/home/ec2-user/Documents/code_on_ec2/new_result'  # ec2
RESULT_DEST_DIR = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/new_result'  # local
OLD_RESULTS_DIR = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/old_results'  # local


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


def send_file(file_path):
    send_command = ' '.join(['scp', '-i', KEY_PAIR_PATH, file_path, EC2_IP+':'+IMG_DEST_DIR])
    print send_command
    subprocess.call(send_command, shell=True)
    return


def move_file(in_file_path, out_file_path):
    move_command = ' '.join(['mv', in_file_path, out_file_path])
    print move_command
    subprocess.call(move_command, shell=True)
    return


def fetch_file():
    fetch_command = ' '.join(['scp', '-i', KEY_PAIR_PATH, EC2_IP+':'+RESULT_SRC_DIR+'/*', RESULT_DEST_DIR])
    print fetch_command
    subprocess.call(fetch_command, shell=True)
    return


def extract_result_file(result_list):
    result_path = result_list[0]
    if result_path[-1] == 'r':
        result_path = result_list[1]
    return result_path


def present_result(result_path):
    # present result
    result_file = open(result_path, 'r')
    result = result_file.read()
    print result
    return


def main():
    # check if a new face image is saved on pi
    new_image_path = check_new_file(IMG_SRC_DIR, 1)
    if new_image_path is not None:
        print 'New face image found!'
        # send it to ec2, and archive it
        new_image_path = new_image_path[0]
        send_file(new_image_path)
        move_file(new_image_path, OLD_IMAGES_DIR)
        print 'Let\'s see who you are...'
        # look for new result
        new_result_present = False
        while not new_result_present:
            fetch_file()
            new_result_list = check_new_file(RESULT_DEST_DIR, 2)
            print new_result_list
            if new_result_list is not None:
                print 'New result found!'
                new_result_present = True
                new_result_path = extract_result_file(new_result_list)
                present_result(new_result_path)
                """
                move_file(new_result_path, OLD_RESULTS_DIR)
                """
            else:
                print 'Still thinking...'
    else:
        print 'Waiting'
    return


def loop():
    print 'Starting ...'
    while True:
        main()
        time.sleep(1)
    return


if __name__ == "__main__":
    main()



