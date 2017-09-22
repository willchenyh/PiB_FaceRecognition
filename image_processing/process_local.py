import cv2

IMG_PATH = "geisel.jpg"


def process(img_path):
    img = cv2.imread(img_path, 0)
    print img.shape
    height, width = img.shape
    img = cv2.resize(img, (width/2, height/2))
    height, width = img.shape
    print img.shape
    img = cv2.rectangle(img, (width/2-50, height/2-50), (width/2+50, height/2+50), 255, 5)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('geisel_new.jpg', img)
    return

def resize(img_path):
    img = cv2.imread(img_path, 1)
    height, width, ch = img.shape
    img = cv2.resize(img, (400, int(height * 400 / width)))
    cv2.imwrite('geisel.jpg', img)


def main():
    process(IMG_PATH)
    return


if __name__ == '__main__':
    main()
