import cv2
import sqlite3

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") #ตัวClassifier

def db_get_name(hospital_id):
    try:
        with sqlite3.connect("PythonDB/hospital_patients.db") as con:
            cur = con.cursor()
            cur.execute("select first_name from patients where hospital_id={}".format(hospital_id))
            first_name = cur.fetchall()
            cur.execute("select last_name from patients where hospital_id={}".format(hospital_id))
            last_name = cur.fetchall()
            return first_name[0][0], last_name[0][0]
    except Exception as e:
        print('Error -> {}'.format(e))

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, clf):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # แปลงภาพเป็นขาวดำเพื่อให้ประหยัดเวลาในการประมวลผล
    features = classifier.detectMultiScale(gray, scaleFactor, minNeighbors) # detectMultiScale คล้ายๆเป็นการ predict, scaleFactor พารามิเตอร์ที่ระบุว่าขนาดภาพจะลดลงเท่าใดในแต่ละขนาดของภาพ
    coords = []

    for (x, y, w, h) in features: # องค์ประกอบแต่ละส่วนภายใน features ที่ทำการ predict มา
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        id, con = clf.predict(gray[y:y + h, x:x + w])

        first_name, last_name = db_get_name(id)
        text = str(id)+'-'+str(first_name)+'-'+str(last_name)

        if con <= 60:
            cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        else:
            cv2.putText(img, "Unknow", (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        if (con < 100):
            con = " {0}%".format(round(100 - con))
        else:
            con = " {0}%".format(round(100 - con))

        print(str(con))
        coords = [x, y, w, h]

    return img, coords

def detect(img, faceCascade, clf):
    img, coords = draw_boundary(img, faceCascade, 1.1, 10, (0, 255, 0), clf)
    if len(coords) == 4: #มีครบ 4 องค์ประกอบ x, y, w, h
        result = img[coords[1]:coords[1] + coords[3], coords[0]:coords[0] + coords[2]] # img[y:y+h, x:x+w]

    return img

img_id = 0
cap = cv2.VideoCapture(0)

clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml")

while (True):
    ret, frame = cap.read()
    frame = detect(frame, faceCascade, clf)
    cv2.imshow('frame', frame)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()



