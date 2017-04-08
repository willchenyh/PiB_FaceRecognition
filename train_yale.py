import numpy as np
from PIL import Image
import os, glob, cv2, time

face_size = (60,60)

def get_image_paths():
    img_path = os.path.join('train', '*.jpg')
    img_path_list = glob.glob(img_path)
    return img_path_list

def get_images_and_labels(face_cascade, path, key):
    img_path_list = get_image_paths()
    face_list = []
    label_list = []
    for img_path in img_path_list:
        img_name = img_path.split('/')[-1]
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_name = img_name.split('.')[0]
        label = int(img_name.split('_')[0])
        print img_name, label
        #label_list.append(label)
        #img = np.array(img, 'uint8')
        #cv2.imwrite('s1.jpg', img)
        print img.shape
        faces = face_cascade.detectMultiScale(img)
        #print faces
        for (x,y,w,h) in faces:
            face = img[y:y+h, x:x+w]
            face = cv2.resize(face, face_size)
            face_list.append(face)
            label_list.append(label)
        #print x, y, w, h, face.shape
        #break
    return face_list, label_list

def train_recognizer(face_cascade):
    print 'reading images'
    t1 = time.time()
    face_list, label_list = get_images_and_labels(face_cascade, 'train', '*jpg')
    t2 = time.time()
    print 'Time for reading images and labels:', t2-t1
    print 'list length:', len(face_list), len(label_list)
    #print label_list
    
    recognizer = cv2.createEigenFaceRecognizer()
    t1 = time.time()
    recognizer.train(face_list, np.array(label_list))
    recognizer.save('willface.xml')
    t2 = time.time()
    print 'Time for training the recognizer:', t2-t1
    print 'training complete'

if __name__ == '__main__':
    
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    train_recognizer(face_cascade)
    print 'done?'
