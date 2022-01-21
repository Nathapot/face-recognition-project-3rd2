import cv2
import numpy as np
from PIL import Image
import os
import sqlite3

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def db_show():
    try:
        with sqlite3.connect("PythonDB/hospital_patients.db") as con:
            con.row_factory = sqlite3.Row
            sql_cmd = "select * from patients"
            for row in con.execute(sql_cmd):
                print(row["hospital_id"], row["first_name"], row["last_name"], row['age'], row['gender'], row['treatment_plan'])
    except Exception as e:
        print('Error -> {}'.format(e))

def db_check(hospital_id):
    try:
        with sqlite3.connect("PythonDB/hospital_patients.db") as con:
            cur = con.cursor()
            cur.execute("select hospital_id from patients where hospital_id={}".format(hospital_id))
            hospital_ids = cur.fetchall()
            return hospital_ids
    except Exception as e:
        print('Error -> {}'.format(e))

def remove_user(user_hospital_id):
    try:
        with sqlite3.connect("/Users/potto/PycharmProjects/hello/PythonDB/hospital_patients.db") as con:
            cur = con.cursor()
            cur.execute("delete from patients where hospital_id={}".format(user_hospital_id))

            print('Removed')
    except Exception as e:
        print('Error -> {}'.format(e))

def add_user(hospital_id, first_name, last_name, age, gender, treatment_plan):
    try:
        with sqlite3.connect("PythonDB/hospital_patients.db") as con:
            cur = con.cursor()
            cur.execute("insert into patients values('{}', '{}', '{}', {}, '{}', '{}')".format(hospital_id, first_name, last_name, int(age), gender, treatment_plan))
            print('Successful!')
    except Exception as e:
        print('Error -> {}'.format(e))

def create_dataset(img, id, img_id):
    cv2.imwrite("data/pic."+str(id)+"."+str(img_id)+".jpg", img)

def delete_dataset(id):
    os.chdir('/Users/potto/PycharmProjects/hello/data')
    for f in os.listdir():
        f_name, f_ext = os.path.splitext(f)
        f_title, f_course, f_num = f_name.split('.')
        if(f_course == str(id)):
            os.remove(f)

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray, scaleFactor, minNeighbors)
    coords = []
    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h),color,2)
        cv2.putText(img, text, (x,y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)
        coords = [x,y,w,h]
    return img, coords

def detect(img, faceCascade, img_id, hospital_id):
    img, coords = draw_boundary(img, faceCascade, 1.1, 10, (0,0,255), "Face")
    if len(coords)==4: #detect
        id = hospital_id
        #img(y:y+h, x:x+w)คืออันข้างล่างนี่ , img เป็นภาพเต็มส่วน result คือภาพตัดที่ตัดมาแต่ตรงหน้าซึ่งตัดมาเฉพาะตอนที่ตรวจจับเจอ
        result = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        create_dataset(result, id,img_id)
    return img

def get_start(hospital_id):
        img_id = 0
        # 2 choice (1. user video 2. use webcam for realtime scan) for this moment i will use webcam
        # cap = cv2.VideoCapture('Sun.mp4')
        cap = cv2.VideoCapture(0)
        while (True):
            ret, frame = cap.read()
            frame = detect(frame, faceCascade, img_id, hospital_id)
            cv2.imshow('frame', frame)
            img_id += 1
            if (cv2.waitKey(1) & 0xFF == ord('q') or img_id == 100):    #img_id ตอนเอาไปใช้จริงจะให้เก็บผู้ป่วยคนละ 500-1000 รูป แต่ตอนสาธิตจะใช้แค่ 100 รูปเพื่อความรวดเร็วในการทดสอบ
                break
        cap.release()
        cv2.destroyAllWindows()
        train_classifier()

# Training
def train_classifier():
    path = [os.path.join ('/Users/potto/PycharmProjects/hello/data', f) for f in os.listdir('/Users/potto/PycharmProjects/hello/data')]
    print(path)
    faces=[]
    ids=[]
    for image in path:
        img = Image.open(image).convert("L")
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split('.')[1])
        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("/Users/potto/PycharmProjects/hello/classifier.xml")
    print('train_successful')

#this part => for nurse or doctor that have to communicate with patients
def get_input():
    hospital_id = input('Please give your hospital id here ')
    hospital_ids = db_check(hospital_id)
    print(f'This is yours hospital id => {hospital_id} ?')
    confirm_by_user = input('Please answer between True or False ')
    confirm_by_users = str(confirm_by_user.upper())
    if(confirm_by_users):
        if(confirm_by_users == 'TRUE'):
            if(hospital_ids != []):
                print('We already have your information')
            else:
                first_name = input('First_name: ')
                last_name = input('Last_name: ')
                age = input('Age: ')
                gender = input('Gender: ')
                treatment_plan = input('Treatment plan: ')
                add_user(hospital_id, first_name, last_name, int(age), gender, treatment_plan)
                get_start(hospital_id)
        else:
            print('Please enter your hospital id again ')

if __name__ == '__main__':
    # train_classifier()

    # choice for user
    choice_for_user = input('1. If you want to start program and import new user Please place (1) '
                            '2. Remove user from database Please place (2) '
                            '3. Show users information Please place (3) ')

    if (choice_for_user == '1'):
        get_input()
    elif (choice_for_user == '2'):
        user_hospital_id = input('Please enter the hospital id for remove user id ')

        remove_user(user_hospital_id)

        delete_dataset(user_hospital_id)
        train_classifier()
        print('Successful removed!')

    elif (choice_for_user == '3'):
        db_show()
    else:
        print('Please contract the staff')








