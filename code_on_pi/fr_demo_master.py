"""
What this script does:
0. assume the local host is already connected to ec2 instance.
1. start running the camera.
2. detect a face, display it, and get confirmation from user.
3. send it for classification and fetch result.
4. show result on face display.
"""

import cv2, glob, os, time
from picamera import PiCamera
from picamera.array import PiRGBArray


CASCADE_PATH = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/haarcascade_frontalface_default.xml'
NEW_FACE_PATH = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/new_face'
NEW_FACE_NAME = 'new_face.jpg'
NEW_IMAGE_PATH = '/home/pi/Documents/myProjects/PIB/face_recognition/code_on_pi/new_image'
NEW_IMAGE_NAME = 'new_image.jpg'
FONT = cv2.FONT_HERSHEY_SIMPLEX


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
    print 'Let me get ready ... 3 seconds ...'
    time.sleep(3)
    print 'Starting ...'

    # 2. detect a face, display it, and get confirmation from user.
    for f in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        frame = f.array
        frame = cv2.resize(frame, (width / 2, height / 2))
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img)
        for (x, y, w, h) in faces:
            if w < 120:
                continue
            # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            face = img[y:y + h + 1, x:x + w + 1]
            face_path = os.path.join(NEW_FACE_PATH, NEW_FACE_NAME)
            cv2.imwrite(face_path, face)
            #image_path = os.path.join(NEW_IMAGE_PATH, NEW_IMAGE_NAME)
            #cv2.imwrite(image_path, img)
            break
        cv2.imshow('Face Image for Classification', frame)
        answer = input('Confirm image? (y/n)')
        if answer == 'y':
            # TODO 3. send it for classification and fetch result.
            # TODO read result
            # display on face image
            result_to_display = 'blabla'
            cv2.putText(frame, result_to_display, (0,0), FONT, 1, (0, 255, 0), 2)
            cv2.imshow('Face Image for Classification', frame)
            # TODO move result file to old dir
            break
        else:
            rawCapture.truncate(0)
    return


if __name__ == '__main__':
    main()
