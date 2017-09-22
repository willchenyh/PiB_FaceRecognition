"""
What this script does:
0. assume the local host is already connected to ec2 instance.
1. start running the camera.
2. detect a face, display it, and get confirmation from user.
3. send it for classification and fetch result.
4. show result on face display.
"""

import cv2, os, time, subprocess
from picamera import PiCamera
from picamera.array import PiRGBArray


CASCADE_PATH = '/home/pi/PiB_FaceRecognition/code_on_pi/haarcascade_frontalface_default.xml'
NEW_FACE_PATH = '/home/pi/PiB_FaceRecognition/code_on_pi/new_face'
NEW_FACE_NAME = 'new_face.jpg'
NEW_RESULT_PATH = '/home/pi/PiB_FaceRecognition/code_on_pi/new_result/result.txt'  # local
FONT = cv2.FONT_HERSHEY_SIMPLEX
EC2_IP = "ec2-user@ec2-52-25-37-56.us-west-2.compute.amazonaws.com"  # ec2 TODO
KEY_PAIR_PATH = "/home/pi/PiB_FaceRecognition/code_on_pi/aws_personal.pem"  # local TODO
IMG_DEST_DIR = '/home/ec2-user/PiB_FaceRecognition/code_on_ec2/new_face'  # ec2
RESULT_SRC_DIR = "/home/ec2-user/PiB_FaceRecognition/code_on_ec2/new_result/result.txt"  # ec2
RESULT_DEST_DIR = "/home/pi/PiB_FaceRecognition/code_on_pi/new_result"  # local


def send_file(file_path):
    send_command = ["scp", "-i", KEY_PAIR_PATH, file_path, EC2_IP+":"+IMG_DEST_DIR]
    #print send_command
    subprocess.call(send_command)
    print 'sending file to server'
    return


def fetch_file():
    fetch_command = ["scp", "-i", KEY_PAIR_PATH, EC2_IP+":"+RESULT_SRC_DIR, RESULT_DEST_DIR]
    while True:
        try:
            subprocess.check_call(fetch_command)
            return NEW_RESULT_PATH
        except subprocess.CalledProcessError:
            continue


def read_result(result_path):
    result_file = open(result_path, 'r')
    result = result_file.read()
    details = result.split(',')
    name = details[0]
    conf = details[1]
    print name, conf
    return name, conf


def main():
    # 1. start running the camera.
    # initialize face detector
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    # initialize camera
    camera = PiCamera()
    width = 640
    height = 480
    camera.rotation = 180
    camera.resolution = (width, height)
    rawCapture = PiRGBArray(camera, size=(width, height))
    # warm up and set up
    print 'Let me get ready ... 2 seconds ...'
    time.sleep(2)
    print 'Starting ...'

    # 2. detect a face, display it, and get confirmation from user.
    for f in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        frame = f.array
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img)
        
        for (x, y, w, h) in faces:
            if w < 120:
                continue
            print '=================================='
            print 'Face detected!'
            cv2.imshow('Face Image for Classification', frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            answer = input('Confirm image (1-yes / 0-no): ')
            print '=================================='
            
            if answer == 1:
                face = img[y:y + h + 1, x:x + w + 1]
                face_path = os.path.join(NEW_FACE_PATH, NEW_FACE_NAME)
                cv2.imwrite(face_path, face)

                # send it for classification and fetch result.
                send_file(face_path)
                os.remove(face_path)
                print 'Let\'s see who you are...'
                # look for new result
                for i in range(3):
                    time.sleep(1)
                    print 'Still thinking...'
                new_result_path = fetch_file()
                print 'New result found!'
                name, conf = read_result(new_result_path)

                # display on face image
                if name == 'Will' and float(conf) > 0.9:
                    result_to_display = 'Hey Will!'
                else:
                    result_to_display = 'Sorry I don\'t know you.'
                cv2.putText(frame, result_to_display, (10,30), FONT, 1, (0, 255, 0), 2)
                cv2.imshow('Face Image for Classification', frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                cv2.waitKey(1)
                cv2.waitKey(1)
                cv2.waitKey(1)
                # remove result
                os.remove(NEW_RESULT_PATH)
                break

        rawCapture.truncate(0)
        print 'Waiting for image...'
        #time.sleep(1)
    return


if __name__ == '__main__':
    main()
