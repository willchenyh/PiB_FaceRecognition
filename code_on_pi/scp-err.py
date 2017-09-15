import subprocess

EC2_IP = 'ec2-user@ec2-52-25-37-56.us-west-2.compute.amazonaws.com'  # ec2 TODO
KEY_PAIR_PATH = '/home/pi/PiB_FaceRecognition/code_on_pi/aws_personal.pem'  # local

command = 'scp -i '+KEY_PAIR_PATH+' '+EC2_IP+':~/ky.py'+' .'
while True:
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        continue
#subprocess.call(command, shell=True)