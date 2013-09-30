"""
File Description

"""
import cv2

def boxes(filename, faces):
    if faces is None:
        print('No faces detected')
        return
    img = cv2.imread(filename)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (127, 255, 0), 1)
    parts = filename.split('.')
    new_name = '%s-detected.%s' % (parts[0], parts[1])
    cv2.imwrite('/tmp/%s' % new_name, img)
    return '/tmp/%s' % new_name


def detect(filename, ratio=1.3, neighbors=4, min_size=(10, 10)):
    img = cv2.imread(filename, 0)
    hc = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    return boxes(filename, hc.detectMultiScale(img, ratio, neighbors, cv2.cv.HAAR_SCALE_IMAGE, min_size))