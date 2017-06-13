import numpy as np
import cv2, glob, os, time
from picamera import PiCamera
from picamera.array import PiRGBArray


if __name__ == '__main__':
    
    # initialize face detector
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # initialize camera
    camera = PiCamera()
    width = 640
    height = 480
    camera.rotation = 180
    camera.resolution = (width,height)#TODO
    rawCapture = PiRGBArray(camera, size=(width,height))

    # initialize values
    counter_begin = 30
    counter_end = 45 # index 1-50 is one lighting condition, 51-100 another.
    counter = counter_begin
    expression = 'frontal3' # normal, smile, sad
    will = '16'
    steven = '17'
    simon = '18'

    # warm up and set up
    print 'Warming Up ... 3 seconds'
    time.sleep(3)
    print 'Starting ...'
    
    for f in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        frame = f.array
        #frame = cv2.resize(frame, (width/2, height/2))
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        '''
        faces = face_cascade.detectMultiScale(img)
        for (x,y,w,h) in faces:
            if w<120:
                continue
            #cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            face = img[y:y+h,x:x+w]
            img_name = 'willfaces/'+will+'_'+expression+'_'+str(counter)+'.jpg'
            cv2.imwrite(img_name, face)
            counter += 1
        '''
        img_name = 'willfaces/will_frontal_3/'+will+'_'+expression+'_'+str(counter)+'.jpg'
        cv2.imwrite(img_name, img)
        counter += 1

        cv2.imshow('Output', frame)
        cv2.waitKey(50)
        
        rawCapture.truncate(0)
        
        print counter
        if counter==counter_end:
            break
