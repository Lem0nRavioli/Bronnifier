import cv2

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
bronn = cv2.imread("faces/bronn_shit.jpg")
bronn = bronn[134:645, 85:558]


def spread_bronn(img_path, save_name, sensitivy=3):
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(img_gray, 1.25, sensitivy)
    for (y, x, h, w) in faces:
        bronn_copy = bronn.copy()
        bronn_copy = cv2.resize(bronn_copy, (w, h))
        img[x:x+w, y:y+h] = bronn_copy
    cv2.imwrite('bronn_paradise/' + save_name + '.jpg', img)
    return img


"""
Save the pictures in the "faces" folder 
Change the path / save name and run
"""

img_path = "faces/<image_name>.jpg"
img_save_name = "<picture_saved_name>"
spread_bronn(img_path, img_save_name)

