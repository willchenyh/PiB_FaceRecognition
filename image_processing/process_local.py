import cv2

IMG_PATH = "geisel.jpg"


def process(img_path):
    img = cv2.imread(img_path, 0)
    height, width, ch = img.shape
    img = cv2.resize(img, (width/2, height/2))
    height, width, ch = img.shape
    cv2.rectangle(img, (width/2-100, height/2-100), (width/2+100, height/2+100), (255,0,0), 10)
    cv2.imwrite('geisel_new.jpg', img)
    return

def resize(img_path)
    img = cv2.imread(img_path, 1)
    height, width, ch = img.shape
    img = cv2.resize(img, (400, int(height * 400 / width)))
    cv2.imwrite('geisel.jpg', img)


def main():
    resize(IMG_PATH)
    process(IMG_PATH)
    return


if __name__ == '__main__':
    main()
