import cv2

IMG_PATH = "geisel.jpg"


def process(img_path):
    img = cv2.imread(img_path, 1)
    height, width = img.shape
    img = cv2.resize(img, (width/2, height/2))
    height, width = img.shape
    cv2.rectangle(img, (width/2-100, height/2-100), (width/2+100, height/2+100), (255,0,0), 20)
    cv2.imwrite('geisel', img)
    return


def main():
    process(IMG_PATH)
    return


if __name__ == '__main__':
    main()
