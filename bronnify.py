import cv2

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

bronn = cv2.imread("bronn_clean.png", cv2.IMREAD_UNCHANGED)
# bronn = bronn[134:670, 85:530]  # trunked top head + chin + thin face
bronn = bronn[90:690, 85:530]  # little cut top of head + chin + thin face


def infect_bronn(pic, face_loc):
    y, x, h, w = face_loc
    face_square = pic[x:x+w, y:y+h].copy()
    bronn_copy = bronn.copy()
    bronn_copy = cv2.resize(bronn_copy, (w, h))

    for i in range(w):
        for j in range(h):
            if bronn_copy[i, j, 3] == 255:
                face_square[i, j] = bronn_copy[i, j, :3]

    pic[x:x+w, y:y+h] = face_square
    return pic


def spread_bronn(img_path, save_name, sensitivity=3):
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(img_gray, 1.25, sensitivity)
    for face in faces:
        img = infect_bronn(img, face)

    cv2.imwrite('bronn_paradise/' + save_name + '.jpg', img)
    return img


"""
Save the pictures in the "faces" folder 
Change the path / save name and run
"""

img_path = "faces/<image_name>.jpg"
img_save_name = "<picture_saved_name>"
spread_bronn(img_path, img_save_name)
