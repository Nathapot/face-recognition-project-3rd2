import cv2

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def create_dataset(img, id, img_id):
    cv2.imwrite("data/pic."+str(id)+"."+str(img_id)+".jpg", img)


def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, clf):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray, scaleFactor, minNeighbors)
    coords = []
    for (x,y,w,h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        id,con = clf.predict(gray[y:y+h, x:x+w]) #ค่าความแม่นยำ

        if con <= 50:
            con2 = "  {:0.2f}%".format(round(100 - con))
            con3 = str(con2)
            cv2.putText(img, "Pot_Nathapot"+" "+con3, (x,y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)
        else:
            cv2.putText(img, "Unknow", (x,y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)
        if(con < 100):
            con = "  {0}%".format(round(100 - con))
        else:
            con = "  {0}%".format(round(100 - con))

        print(str(con))

        coords = [x,y,w,h]
    return img, coords

def detect(img, faceCascade, img_id, clf):
    img, coords = draw_boundary(img, faceCascade, 1.1, 10, (0,0,255), clf)
    if len(coords)==4: #detect
        id=1
        #img(y:y+h, x:x+w)คืออันข้างล่างนี่ , img เป็นภาพเต็มส่วน result คือภาพตัดที่ตัดมาแต่ตรงหน้าซึ่งตัดมาเฉพาะตอนที่ตรวจจับเจอ
        result = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
    return img

img_id = 0
cap = cv2.VideoCapture(0)



clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml")

while (True):
    ret,frame = cap.read()
    frame = detect(frame, faceCascade, img_id, clf)
    cv2.imshow('frame', frame)
    img_id+=1
    if(cv2.waitKey(1) & 0xFF==ord('q')):
        break
cap.release()
cv2.destroyAllWindows()



