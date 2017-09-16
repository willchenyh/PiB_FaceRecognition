import cv2

IMG_PATH = "geisel.jpg"


def process(img_path):
    img = cv2.imread(img_path, 0)
    height, width = img.shape
    img = cv2.resize(img, (height/2, width/2))
    height, width = img.shape
    cv2.rectangle(img, (height-5, width-5), (height+5, width+5), (255,0,0), 2)
    cv2.imwrite('geisel_new.jpg', img)
    return


def main():
    process(IMG_PATH)
    return


if __name__ == '__main__':
    main()
