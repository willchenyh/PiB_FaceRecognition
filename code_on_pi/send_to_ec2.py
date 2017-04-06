"""
What this script does:
0. assume the local host is already connected to ec2 instance
1. check if a new face image is saved in IMG_SRC_DIR.
2. send image to ec2 instance's IMG_DEST_DIR.
3. change name and move the image to OLD_IMAGES_DIR.
4. check if a new result is saved in RESULT_DEST_DIR.
5. read and present result
"""

import glob, os, subprocess

IMG_SRC_DIR = '/home/willchen/Documents/pib/code_on_pi/new_face' # local
IMG_DEST_DIR = '/home/ec2-user/Documents/code_on_ec2/new_face' # ec2
KEY_PAIR_PATH = '/home/willchen/Documents/pib/pib_fr.pem' # local
EC2_IP = 'ec2-user@ec2-35-167-141-186.us-west-2.compute.amazonaws.com' # ec2
OLD_IMAGES_DIR = '/home/willchen/Documents/pib/code_on_pi/old_faces' # local
RESULT_SRC_DIR = '/home/ec2-user/Documents/code_on_ec2/new_result' # ec2
RESULT_DEST_DIR = '/home/willchen/Documents/pib/code_on_pi/new_result' # local

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

def send_file(file_path):
    send_command = ' '.join(['scp', '-i', KEY_PAIR_PATH, file_path, EC2_IP+':'+IMG_DEST_DIR])
    print send_command
    subprocess.call(send_command, shell=True)
    return

def move_file(file_path):
    move_command = ' '.join(['mv', file_path, OLD_IMAGES_DIR])
    print move_command
    subprocess.call(move_command, shell=True)
    return

def fetch_file():
    fetch_command = ' '.join(['scp', '-i', KEY_PAIR_PATH, EC2_IP+':'+RESULT_SRC_DIR+'/*', RESULT_DEST_DIR])
    print fetch_command
    subprocess.call(fetch_command, shell=True)
    return

def present_result(result_path):
    # present result
    return

def main():
    # if a new face image is saved, send it to ec2 instance
    new_image_path = check_new_file(IMG_SRC_DIR, 1)
    if new_image_path is not None:
        print 'New face image found!'
	new_image_path = new_image_path[0]
        send_file(new_image_path)
        move_file(new_image_path)
	print 'Let\'s see who you are...'
        # look for new result
        new_result_present = False
        while not new_result_present:
	    fetch_file()
            new_result_path = check_new_file(RESULT_DEST_DIR, 2)
	    print new_result_path
	    if new_result_path is not None:
		print 'New result found!'
                new_result_present = True
                present_result(new_result_path)
	    else:
		print 'Still thinking...'
    return

if __name__ == "__main__":
    main()



