import sqlite3 as It

# เชื่อมต่อฐานข้อมูล hospital_patients
con = It.connect('hospital_patients.db')
with con:
    cur = con.cursor()  #ตัว pointer
    # พอสร้างไว้แล้วต้องปิดทิ้งไม่งั้นมันจะ error เพราะเรามีตารางอยู่แล้ว
    cur.execute("create table patients(hospital_id text, first_name text, last_name text, age int, gender text,treatment_plan text )")
    # mock ข้อมูลมา test
    cur.execute("insert into patients values('61010283', 'Nathapot', 'Pornpitakpan', 22, 'Male','A')")
    cur.execute("insert into patients values('61010215', 'Charun', 'Setsiriphaibun', 20, 'Male', 'B')")
    cur.execute("insert into patients values(61010152, 'Jirat', 'Kunpreeyawat', 20, 'Male', 'C')")
    cur.execute("insert into patients values(61010208, 'Chayaroq', 'Lawanwisut', 21, 'Male', 'D')")

    # ใส่เข้ามาพร้อมกันเป็น list ใน list ที่ index ต่างๆก็จะเป็น tuple
    # hospital_ids = [(61010283, 'ณฐพศ', 'พรพิทักษ์พันธุ์', 22, 'ชาย','แผนการรักษา A'),
    #                 (61010215, 'ชรัณ', 'เศรษฐศิริไพบูลย์', 20, 'ชาย', 'แผนการรักษา B'),
    #                 (61010152, 'จิรัฐฎ์', 'ควรปรียาวัฒน์', 20, 'ชาย', 'แผนการรักษา C'),
    #                 (61010208, 'ชยรพ', 'ลาวัณวิสุทธิ์', 21, 'ชาย', 'แผนการรักษา D')]
    # cur.executemany("insert into patients values(?, ?, ?, ?, ?, ?)", hospital_ids)

    # เอาข้อมูลมาโชว์
    # cur.execute("select * from patients")
    # row = cur.fetchall() #ถ้าเป็น fetchone ก็จะเอาแค่ตัวแรกมาโชว์
    # print(row) # ถ้าจะชี้ก็ระบุตำแหน่ง index ลง ไปเช่น row[0][0] ไรงี้

    # delete ข้อมูล
    # cur.execute("delete from patients where hospital_id=61010152")

    # delete all
    # cur.execute("delete from patients")

    # update ข้อมูล
    # cur.execute("update patients set first_name='ชรัณ' where hospital_id=61010215")


con.close()
