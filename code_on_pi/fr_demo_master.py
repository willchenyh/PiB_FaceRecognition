"""
What this script does:
0. assume the local host is already connected to ec2 instance.
1. start running the camera.
2. detect a face, display it, and get confirmation from user.
3. send it for classification and fetch result.
4. show result on face display.
"""

import cv2, os, time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import send_to_ec2


CASCADE_PATH = '/home/pi/PiB_FaceRecognition/code_on_pi/haarcascade_frontalface_default.xml'
NEW_FACE_PATH = '/home/pi/PiB_FaceRecognition/code_on_pi/new_face'
NEW_FACE_NAME = 'new_face.jpg'
NEW_RESULT_PATH = '/home/pi/PiB_FaceRecognition/code_on_pi/new_result/result.txt'  # local
OLD_RESULTS_DIR = '/home/pi/PiB_FaceRecognition/code_on_pi/old_results'  # local
SEND_FILE_COMMAND = 'python /home/pi/Documents/PIB/code_on_pi/send_to_ec2.py'
FONT = cv2.FONT_HERSHEY_SIMPLEX

"""
def move_file(in_file_path, out_file_path):
    move_command = ' '.join(['mv', in_file_path, out_file_path])
    print move_command
    os.system(move_command)
    return
"""

def main():
    # 1. start running the camera.
    # initialize face detector
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    # initialize camera
    camera = PiCamera()
    width = 640
    height = 480
    camera.rotation = 180
    camera.resolution = (width, height)  # TODO
    rawCapture = PiRGBArray(camera, size=(width, height))
    # warm up and set up
    print 'Let me get ready ... 2 seconds ...'
    time.sleep(2)
    print 'Starting ...'

    # 2. detect a face, display it, and get confirmation from user.
    for f in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        frame = f.array
        img = cv2.resize(frame, (width / 2, height / 2))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img)
        
        for (x, y, w, h) in faces:
            if w < 120:
                continue
            print 'Face detected'
            # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            face = img[y:y + h + 1, x:x + w + 1]
            face_path = os.path.join(NEW_FACE_PATH, NEW_FACE_NAME)
            cv2.imwrite(face_path, face)
            #image_path = os.path.join(NEW_IMAGE_PATH, NEW_IMAGE_NAME)
            #cv2.imwrite(image_path, gimg)
            
            cv2.imshow('Face Image for Classification', frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            answer = input('Confirm image (1-yes / 0-no): ')
            
            if answer == 1:
                # send it for classification and fetch result.
                #os.system(SEND_FILE_COMMAND)
                name, conf = send_to_ec2.main()

                # display on face image
                if name == 'Will' and float(conf) > 0.9:
                    result_to_display = 'Hey Will!'
                else:
                    result_to_display = 'Sorry I don\'t know you.'
                bg = np.zeros((frame.shape[0]+30, frame.shape[1]))
                bg[30:, :] = frame
                cv2.putText(bg, result_to_display, (10,30), FONT, 1, (0, 255, 0), 2)
                cv2.imshow('Face Image for Classification', frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                cv2.waitKey(1)
                cv2.waitKey(1)
                cv2.waitKey(1)
                # remove result
                #shutil.move(NEW_RESULT_PATH, OLD_RESULTS_DIR)
                os.remove(NEW_RESULT_PATH)
                break

        rawCapture.truncate(0)
        print 'Waiting ...'
        time.sleep(2)
    return


if __name__ == '__main__':
    main()
