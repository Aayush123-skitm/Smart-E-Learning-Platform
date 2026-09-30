import csv      
import cv2
import smtplib
from email.message import EmailMessage
import random
import re
import os  
from google.genai import types
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI                                   
from PIL import Image,ImageDraw,ImageFont
import time                    
import random
from db import con,cursor

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

mai_folder = os.path.join(BASE_FOLDER, "study_material")

load_dotenv()

openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# os.makedirs(main_folder, exist_ok=True)
def send_certificate_email(student_email, certificate_file):

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    msg = EmailMessage()

    msg["From"] = sender_email
    msg["To"] = student_email
    msg["Subject"] = "Smart E-Learning | Course Certificate"

    msg.set_content("""
Hello Learner 👋,

Congratulations! 🎉

Your course certificate is attached with this email.

Thank you for learning with Smart E-Learning.

Best Regards,
Smart E-Learning Team
""")

    with open(certificate_file, "rb") as f:
        certificate_data = f.read()

    msg.add_attachment(
        certificate_data,
        maintype="application",
        subtype="pdf",
        filename="Smart_E-Learning_Certificate.pdf"
    )

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("Certificate sent successfully to your email.")

    except Exception as e:
        print("Certificate sending failed:", e)
        
        
        ################ starting
while True:
    print("\nSMART E-LEARNING & QUIZ SYSTEM")
    ti = input("STUDENT(0) OR ADMIN(2) = ")
    if ti =="0":
        a = input("REGISTER OR LOGIN = ").lower() #students register 
        

        if a=="r":
            name = input("ENTER YOUR FULL NAME = ")
            # Check  student is already registered
            sql = "SELECT student_id FROM students WHERE name = %s"
            cursor.execute(sql, (name,))
            existing_student = cursor.fetchone()

            if existing_student:
                print("=" * 38)
                print(" YOU ARE ALREADY REGISTERED!")
                print(" Please login instead.")
                print("=" * 38)
    
            else:
                while True:
                    em = input("ENTER YOUR EMAIL = ")
                    score = 0
                    # @ check
                    if re.search(r"@", em):
                        score += 1
                    # username @ se pehle hona chahiye
                    if re.search(r"^[^@\s]+@", em):
                        score += 1
                    # @ ke baad .com hona chahiye
                    if re.search(r"@[^@\s]+\.com$", em):
                        score += 1
                    # space nahi hona chahiye
                    if " " not in em:
                        score += 1
                    if score < 4:
                        print("Invalid Email.")
                    else:
                        characters = "ABCDEFGHI123tuvrs4567890#@"

                        otp = ''.join(random.choices(characters, k=random.randint(4,6)))
                        otp_time = time.time()

                        sender_email = os.getenv("SENDER_EMAIL")
                        sender_password = os.getenv("SENDER_PASSWORD")
 
                        msg = EmailMessage()

                        msg["From"] = sender_email
                        msg["To"] = em
                        msg["Subject"] = "Smart E-Learning | Email Verification OTP"

                        msg.set_content(f"""
Hello Learners 👋,

Welcome to Smart E-Learning!

Your One-Time Password (OTP) for registration is:

OTP: {otp}

This OTP is valid for 2 minutes.
Please do not share this OTP with anyone.

If you did not request this registration, please ignore this email.

Best Regards,
Smart E-Learning Team
College Learning & Quiz Platform
""")



                        try:
                            server = smtplib.SMTP("smtp.gmail.com", 587)
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.send_message(msg)
                            server.quit()

                            print("OTP sent successfully to your email.")

                        except Exception as e:
                            print("OTP sending failed:", e)
                            continue
                        user_otp = input("ENTER OTP = ")

                        current_time = time.time()

                        if current_time - otp_time > 120:
                            print("OTP EXPIRED. Please request a new OTP.")

                        elif user_otp == otp:
                            print("EMAIL VERIFIED SUCCESSFULLY.")
                            break

                        else:
                            print("WRONG OTP. Please try again.") 
                while True:
                    sp = input("SET PASSWORD = ")
                    score = 0
                    if len(sp)>=8:
                        score +=1
                    if re.search(r"[a-z]",sp):
                        score+=1
                    if re.search(r'[A-Z]',sp):
                        score+=1    
                    if re.search(r'[0-9]',sp):
                        score+=1     
                    if score < 4:
                        print("weak")
                    else:
                        break        
                pn = int(input("ROLL NUMBER (eg.01 aur 02 , not abcd01)= "))
                cn = input("ENTER YOUR COLLEGE NAME = ")
                cr= input("COURSE NAME = ")
                br = input("BRANCH NAME = ")
                print("SECURITY QUESTIONS")
                fi= (input("WHAT IS YOUR DOB (EG.01NOVEMBER2005)= "))

                sql = """
                insert into students
                (Name, Email, set_pss, ph_no, clg_name, course, branch, secu_ans)
                values (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (name, em, sp, pn, cn, cr, br, fi)
                cursor.execute(sql,data)
                con.commit() 
                print("REGISTER SUCCESSFULL.")

        elif a=="l":
            nm = input("ENTER YOUR NAME = ") #students login
            ps = input("ENTER YOUR PASSWORD (if you lost you password press 3)= ")
            if ps == "3":
                print("SECURITY QUESTIONS")

                p = input("WHAT IS YOUR DOB = ")

                sql = """
                SELECT * FROM students
                WHERE Name = %s AND secu_ans = %s
                """

                data = (nm, p)

                cursor.execute(sql, data)
                result = cursor.fetchone()

                if result:

                    print("IF YOU CHECK YOUR PASSWORD CLICK 1.")

                    c = input("ENTER YOUR CHOICE = ")

                    if c == "1":
                        sql = """
                        SELECT student_id, Name, Email, set_pss, ph_no,
                            clg_name, course, branch
                        FROM students
                        WHERE Name = %s
                        """

                        data = (nm,)
                        cursor.execute(sql, data)
                        ec = cursor.fetchall()

                        if ec:

                            row = ec[0]

                            # Database wali email
                            em = row[2]
                            characters = "ABCDEFGHI123tuvrs4567890#@"

                            otp = ''.join(random.choices(characters, k=random.randint(4,6)))
                            otp_time = time.time()

                            sender_email = os.getenv("SENDER_EMAIL")
                            sender_password = os.getenv("SENDER_PASSWORD")

                            msg = EmailMessage()

                            msg["From"] = sender_email
                            msg["To"] = em
                            msg["Subject"] = "Smart E-Learning | Details Verification OTP"

                            msg.set_content(f"""
Hello Learner 👋,

Welcome to Smart E-Learning!

Your OTP to view your account details is:

OTP: {otp}

This OTP is valid for 2 minutes.
Please do not share this OTP with anyone.

If you did not request this, please ignore this email.

Best Regards,
Smart E-Learning Team
College Learning & Quiz Platform
""")
                            try:

                                server = smtplib.SMTP("smtp.gmail.com", 587)
                                server.starttls()
                                server.login(sender_email, sender_password)
                                server.send_message(msg)
                                server.quit()

                                print("\nOTP sent successfully to your registered email.")

                            except Exception as e:

                                print("OTP sending failed:", e)

                            else:
                                user_otp = input("ENTER OTP = ")

                                current_time = time.time()

                                if current_time - otp_time > 120:

                                    print("OTP EXPIRED. Please try again.")

                                elif user_otp == otp:

                                    print("EMAIL VERIFIED SUCCESSFULLY.")
                                    print("=" * 38)
                                    print("       YOUR DETAIL IS")
                                    print("=" * 38)

                                    print("| Id           :", row[0])
                                    print("| Name         :", row[1])
                                    print("| Email        :", row[2])
                                    print("| Password     :", row[3])
                                    print("| Roll Number  :", row[4])
                                    print("| College      :", row[5])
                                    print("| Course       :", row[6])
                                    print("| Branch       :", row[7])

                                    print("=" * 38)

                                else:

                                    print("WRONG OTP. DETAILS CANNOT BE SHOWN.")

                        else:
                            print("STUDENT DETAILS NOT FOUND.")

                    else:
                        print("NOT VALID CHOICE")

                else:
                    print("WRONG NAME OR SECURITY ANSWER.")
            else:
                sql="""
                select * from students 
                where name = %s AND set_pss = %s    
                """
                data = (nm, ps)
                cursor.execute(sql, data)
                ec = cursor.fetchone()
                if ec:
                    student_id = ec[0]
                    name = ec[1]
                    print("LOGIN SUCCESSFULLY.")
                    while True:
                       
                        print("\n 1.Your Detail. \n 2.Check Result. \n 3.Course List \n 4.Check Certificate. \n 5.learn using Videos & PDF's \n 6.Give Quiz. \n 7.Announcements. \n 8.Feedback. \n 9.Interview practice. \n 10.Exit \n")
                        c=input("ENTER YOUR CHOICE = ")
                        if c=="2":
                            print("=" * 38)
                            print("      YOUR RESULT IS.")
                            print("=" * 38)
                            sql="""
                            select result_id, name, subject, tq, score, percentage, status, medium, st_0f_certi from result 
                            where name = %s     
                            """
                            data = (nm,)
                            cursor.execute(sql, data)
                            ec = cursor.fetchall()
                            for row in ec:
                                print("-" * 38)
                                print("Name                  :",row[1])
                                print("Result Id             :",row[0])
                                print("Subject               :",row[2])
                                print("Total Question        :",row[3])
                                print("Score                 :",row[4])
                                print("Percentage            :",row[5])
                                print("Status                :",row[6])
                                print("Medium                :",row[7])
                                print("Status Of Certifcate  :",row[8])
                        elif c=="1":
                          
                            print("=" * 38) 
                            print("      YOUR DETAIL IS")
                            print("=" * 38)
                            sql="""
                            select student_id, Name, Email, set_pss, ph_no, clg_name, course, branch from students
                            where name = %s
                            """           
                            data = (nm,)
                            cursor.execute(sql,data)
                            ec=cursor.fetchall()
                            
                            for row in ec:
                                
                                print("-" * 38)
                               
                                print("Id            :",row[0])
                                print("Name          :",row[1])
                                print("Email         :",row[2])
                                print("Password      :",row[3])
                                print("Roll Number   :",row[4])
                                print("College       :",row[5])
                                print("Course        :",row[6])
                                print("Branch        :",row[7])
                        elif c=="3":
                            print("-" * 38)
                            print("\n 1.Python \n 2.Java \n 3.C \n 4.CPP \n 5.HTML \n 6.DBMS \n 7.Aptitude \n 8.Machine Learning \n 9.Natural Language Processing \n ")
                            print("-" * 38)   
                        elif c=="4":
                                sid = student_id
                                print("=" * 38)
                                print("       YOUR CERTIFICATES")
                                print("=" * 38)

                                sql = """
                                SELECT certi_id, subject, score, status, certi_file
                                FROM certificate
                                WHERE student_id = %s
                                """

                                cursor.execute(sql, (sid,))
                                certificates = cursor.fetchall()

                                if certificates:
                                    for row in certificates:
                                        print("\n-------------------------------")
                                        print("Certificate ID :", row[0])
                                        print("Subject        :", row[1])
                                        print("Score          :", row[2])
                                        print("Status         :", row[3])
                                        # print("File           :", row[4])

                                    cert_choice = int(input("\nEnter Certificate ID to open : "))
                                    

                                    sql = """
                                    SELECT certi_file
                                    FROM certificate
                                    WHERE certi_id = %s AND student_id = %s
                                    """

                                    cursor.execute(sql, (cert_choice, sid))
                                    cert = cursor.fetchone()

                                    if cert:
                                        pdf_path = cert[0]

                                        if os.path.exists(pdf_path):
                                            print("\nOpening Certificate...")
                                            os.startfile(pdf_path)
                                        else:
                                            print("Certificate file not found.")
                                    else:
                                        print("Invalid Certificate ID.")

                                else:
                                    print("You don't have any certificate.")        
                        elif c=="5":
                            sub = input("subject = ").lower().strip().strip("'\"")

                            fol = os.path.join(mai_folder, sub)
                            print("For Video press 1. \nFor PDF Press 2. ")
                            cs = int(input("Choice = "))

                            if cs==2:
                                pdf = os.path.join(fol, f"{sub}_Basic_Notes.pdf")

                                print("\nChecking:")
                                print(pdf)

                                if os.path.exists(pdf):
                                    print("\nOpening pdf...")
                                    os.startfile(pdf)
                                else:
                                    print("\nFile not found!")
                                    print("Expected file:", pdf)
                            elif cs==1:
                                videos = []

                                for file in os.listdir(fol):
                                    if file.endswith(".mp4"):
                                        videos.append(file)
                                if len(videos) == 0:
                                    print("\nNo videos available for", sub)
                                else:        
                                    print("\nAvailable Videos:")
                                    for i, file in enumerate(videos, 1):
                                        print(i, file)

                                    gf = int(input("\nWhich video = "))

                                    pdf = os.path.join(fol, videos[gf-1])

                                    print("Checking:")
                                    print(pdf)

                                    if os.path.exists(pdf):
                                        print("Opening video...")
                                        os.startfile(pdf)
                                    else:
                                        print("\nFile not found!")        
                            else:
                                print("Wrong Choice")    
                        elif c=="6":
                        # SUBJECT SELECTED 
                            print("\n===== SELECT SUBJECT =====")
                            print("\n 1.Python \n 2.Java \n 3.C \n 4.CPP \n 5.HTML \n 6.DBMS \n 7.Aptitude \n 8.Machine Learning \n 9.Natural Language Processing \n ")
                            print("========INSTRUCTION======== \n 1.Minus Marking \n 2.Time gives Only 15 Minutes \n ")
                            # name = input("ENTER YOUR NAME = ")    
                            
                            name = name
                            sub = input("ENTER YOUR SUBJECT = ").lower()
                            me ="EASY"
                            sid = student_id
                            qu=[]
                            
                            match sub:
                                case "python":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e)    
                                ############### java    #####################################################3    
                                case "java":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e) 
                                        
                #################### c language #########################                                                        
                                case "c":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e) 
                    ##################3 CPP #########################
                                case "cpp":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e) 
                    ############################# html ######
                                case "html":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e) 
                ##############################  DBMS ############
                                case "dbms":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e)                                                                                                            
    ################################## aptitude ###################
                                case "aptitude":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e) 
    ########################################3333 ML #############################################3
                                case "ml":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e) 
        ######################### NLP #########################
                                case "nlp":
                                    qu = []
                                    with open(os.path.join(BASE_FOLDER, "python.csv"), "r", newline="") as f:
                                        read = csv.DictReader(f)

                                        for row in read:
                                            qu.append(row)

                                    # Random questions
                                    qq = random.sample(qu, 5)

                                    score = 0
                                    correct = 0
                                    wrong = 0
                                    skipped = 0
                                    quiz_history = []

                                    start = time.time()
                                    limit = 600

                                    for q in qq:
                                        use_time = time.time() - start
                                        remaining = limit - use_time

                                        if use_time >= limit:
                                            print("\nTIME OVER!")
                                            break

                                        print("\n" + "=" * 50)
                                        print("Q.", q["qus"])
                                        print("A.", q["op_a"])
                                        print("B.", q["op_b"])
                                        print("C.", q["op_c"])
                                        print("D.", q["op_d"])
                                        print("=" * 50)

                                        print("If you do not know the answer, type SKIP.")

                                        ans = input("ENTER YOUR ANSWER (A/B/C/D) = ").lower()

                                        #SKIP

                                        if ans == "skip":

                                            print("Question Skipped! No marks deducted.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "SKIPPED",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})

                                            continue

                                        if ans not in ["a", "b", "c", "d"]:
                                            print("Invalid answer! Question skipped.")

                                            skipped += 1

                                            quiz_history.append({
                                                "question": q["qus"],
                                                "op_a": q["op_a"],
                                                "op_b": q["op_b"],
                                                "op_c": q["op_c"],
                                                "op_d": q["op_d"],
                                                "user_answer": "INVALID",
                                                "correct_answer": q["correct_ans"],
                                                "status": "SKIPPED"})
                                            continue

                                        USER_ANS = "op_" + ans

                                        if USER_ANS == q["correct_ans"]:

                                            print("Your Answer Is Correct")

                                            score += 1
                                            correct += 1
                                            status = "CORRECT"

                                        else:

                                            print("Your Answer Is Incorrect")
                                            print("Correct Answer Is", q["correct_ans"])

                                            score -= 0.25
                                            wrong += 1
                                            status = "WRONG"

                                        # Save question history
                                        quiz_history.append({
                                            "question": q["qus"],
                                            "op_a": q["op_a"],
                                            "op_b": q["op_b"],
                                            "op_c": q["op_c"],
                                            "op_d": q["op_d"],
                                            "user_answer": USER_ANS,
                                            "correct_answer": q["correct_ans"],
                                            "status": status})
                                        #RESULT

                                    print("\n==============================")
                                    print("TOTAL QUESTIONS :", len(qq))
                                    print("CORRECT ANSWERS :", correct)
                                    print("WRONG ANSWERS   :", wrong)
                                    print("SKIPPED         :", skipped)
                                    print("YOUR SCORE      :", score, "/", len(qq))

                                    percentage = (score / len(qq)) * 100

                                    print("PERCENTAGE      :", percentage)
                                    print("==============================")
                                    # PASS / CERTIFICATE
                                    

                                    if percentage >= 45:
                                        ST = "PASS"
                                        print("\nYOU ARE PASS")
                                        tt = int(time.time() - start)
                                        cert = "Genrated"

                                        sql = """
                                        INSERT INTO result
                                        (student_id, subject, tq, score, percentage,
                                        time_taken, status, medium, name, st_0f_certi)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """

                                        data = (sid,sub,len(qq),score,percentage,tt,ST,me,name,cert)
                                        cursor.execute(sql, data)
                                        con.commit()
                                        print("Result Saved.")
                                        nss = name
                                        QUIZ = sub

                                        sql = """
                                        SELECT certi_id, certi_file
                                        FROM certificate
                                        WHERE student_id = %s AND subject = %s
                                        """
                                        cursor.execute(sql, (sid, sub))
                                        existing_certificate = cursor.fetchone()
                                        if existing_certificate:

                                            print("\n======================================")
                                            print("CERTIFICATE ALREADY GENERATED!")
                                            print("You already have a certificate for", sub)
                                            print("======================================")

                                        else:

                                            base_folder = os.path.dirname(os.path.abspath(__file__))
                                            certificate_folder = os.path.join(base_folder, "certificates")

                                            os.makedirs(certificate_folder, exist_ok=True)
                                            print("Current folder:", os.getcwd())

                                            cerpy_path = os.path.join(BASE_FOLDER, "cerpy.png")
                                            cerp = Image.open(cerpy_path)
                                            draw = ImageDraw.Draw(cerp)
                                            font_path = os.path.join(BASE_FOLDER, "Boldonse-Regular.ttf")
                                            font = ImageFont.truetype(font_path, 38)
                                            # ================= NAME CENTER =================

                                            bbox = draw.textbbox((0, 0), nss, font=font)

                                            name_width = bbox[2] - bbox[0]

                                            name_x = (cerp.width - name_width) // 2

                                            draw.text((name_x, 644),nss,fill="black",font=font)
                                            # ================= COURSE CENTER =================

                                            bbox = draw.textbbox((0, 0), QUIZ, font=font)

                                            course_width = bbox[2] - bbox[0]

                                            course_x = (cerp.width - course_width) // 2

                                            draw.text((course_x, 873),QUIZ,fill="black",font=font)
                                            pdf_path = os.path.join(certificate_folder,f"{nss}_{QUIZ}.pdf")
                                            cerp.convert("RGB").save(pdf_path)
                                            print(f"CERTIFICATE GENRATOR FOR THE {nss}")
                                            # SAVE CERTIFICATE DETAILS IN CERTIFICATE TABLE
                                            sql = """
                                            INSERT INTO certificate
                                            (student_id, subject, score, status, certi_file)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """

                                            data = (sid,sub,score,ST,pdf_path)

                                            cursor.execute(sql, data)
                                            con.commit()

                                            print("Certificate details saved in database.")
                                            ###### certificate send by email (((((( ERROR NICK))))))
                                            student_email = ec[2]

                                            send_certificate_email(student_email, pdf_path)
                                    else:
                                        print("YOU ARE NOT ELIGIBLE FOR CERTIFICATE.") 
                                    view = input("\nDo you want to view your questions? (Y/N) = ").lower()

                                    if view == "y":

                                        for i, item in enumerate(quiz_history, start=1):

                                            print("\n" + "=" * 55)
                                            print("QUESTION", i)
                                            print("=" * 55)

                                            print(item["question"])

                                            print("A.", item["op_a"])
                                            print("B.", item["op_b"])
                                            print("C.", item["op_c"])
                                            print("D.", item["op_d"])

                                            print("\nYour Answer   :", item["user_answer"])
                                            print("Correct Answer:", item["correct_answer"])
                                            print("Status        :", item["status"])

                                            # AI SOLUTION

                                            solution = input("\nDo you want full solution? (Y/N) = ").lower().strip()

                                            if solution == "y":
                                                print("\nSOLUTION:\n")

                                                try:
                                                    correct_option = item["correct_answer"]

                                                    if correct_option == "op_a":
                                                        correct_text = item["op_a"]
                                                    elif correct_option == "op_b":
                                                        correct_text = item["op_b"]
                                                    elif correct_option == "op_c":
                                                        correct_text = item["op_c"]
                                                    else:
                                                        correct_text = item["op_d"]

                                                    prompt = f"""
                                Give a very short and simple solution for this Python quiz question.

                                Question:
                                {item["question"]}

                                Correct Answer:
                                {correct_text}

                                Rules:
                                - Explain in only 2 to 4 short lines.
                                - Use very simple English.
                                - If useful, give a tiny Python example.
                                - Do not add headings.
                                - Do not make the explanation lengthy.
                                """

                                                    response = openrouter_client.chat.completions.create(
                                                        model="openrouter/free",
                                                        messages=[
                                                            {
                                                                "role": "user",
                                                                "content": prompt
                                                            }
                                                        ]
                                                    )

                                                    print(response.choices[0].message.content)

                                                except Exception as e:

                                                    print("Solution could not be generated:", e) 
                                        
                        elif c=="7":
                            sql = """
                            select * from announce
                            """
                            cursor.execute(sql)
                            ac = cursor.fetchall()
                            print("\n")
                            if ac:
                                print("========== ANNOUNCEMETS ==========")
                                for row in ac:
                                    print("Announcement ID : ",row[0])
                                    print("Title           : ",row[1])
                                    print("Message         : ",row[2])
                                    print("Date            : ",row[3])
                                    print("Status          : ",row[4])
                                    print("-" * 34)
                                print("=" * 34)
                                        
                        elif c=="8":
                            print("=" * 34)     
                            sd = student_id
                            nme = ec[1]
                            mes = input("ENTER YOUR FEEDBACK = ")
                            sql = """
                            insert into feedback
                            (student_id, Name, msg)
                            values (%s, %s, %s)
                            """
                            data = (sd, nme, mes)
                            cursor.execute(sql, data)
                            con.commit()
                            print("THANKYOU FOR FEEDBACK")
                            
                        elif c=='9':


                            print("\n")
                            print("=" * 60)
                            print("             HR INTERVIEW PRACTICE")
                            print("=" * 60)

                            print("\n1. Tell me about yourself")
                            print("2. What are your strengths?")
                            print("3. What are your weaknesses?")
                            print("4. Why should we hire you?")
                            print("5. Why do you want to join our company?")
                            print("6. Where do you see yourself in 5 years?")
                            print("7. How do you handle pressure?")
                            print("8. Are you comfortable working in a team?")
                            print("9. What are your career goals?")
                            print("10. Do you have any questions for us?")
                            print("11. Exit")

                            q = input("\nEnter your choice : ")

                            if q == '11':

                                print("\nExiting HR Interview...")

                            elif q in ['1', '2', '3', '4', '5',
                                    '6', '7', '8', '9', '10']:

                                if q == '1':
                                    selected_question = "Tell me about yourself"

                                elif q == '2':
                                    selected_question = "What are your strengths?"

                                elif q == '3':
                                    selected_question = "What are your weaknesses?"

                                elif q == '4':
                                    selected_question = "Why should we hire you?"

                                elif q == '5':
                                    selected_question = "Why do you want to join our company?"

                                elif q == '6':
                                    selected_question = "Where do you see yourself in 5 years?"

                                elif q == '7':
                                    selected_question = "How do you handle pressure?"

                                elif q == '8':
                                    selected_question = "Are you comfortable working in a team?"

                                elif q == '9':
                                    selected_question = "What are your career goals?"

                                elif q == '10':
                                    selected_question = "Do you have any questions for us?"

                                print("\n")
                                print("=" * 60)
                                print("                                QUESTION")
                                print("=" * 60)

                                print("\n", selected_question)

                                # -------------------------------------------------
                                # OPENROUTER PROMPT
                                # -------------------------------------------------

                                prompt = f"""
                                You are an HR interview coach jo ek college student ko real HR
                                interview ke liye prepare kar raha hai.

                                Interview Question:
                                {selected_question}

                                Tumhara kaam hai student ko ye samjhana ki is specific interview
                                question ka answer HOW dena chahiye aur uske baad ek natural
                                SAMPLE ANSWER dena hai.

                                IMPORTANT:
                                Answer selected question ke according hi hona chahiye.
                                Har question ke liye same answer structure use mat karo.

                                Use EXACTLY these sections:

                                ============================================================
                                HOW TO ANSWER
                                ============================================================

                                Answer ko clear point-by-point format mein do.

                                Question ke according 4 se 6 useful points do.

                                Har point mein:
                                • Candidate ko kya bolna chahiye, ye explain karo.
                                • Explanation short rakho.
                                • Practical speaking advice do.
                                • Simple English use karo.

                                Structure question ke according change hona chahiye.

                                Examples:

                                For "Tell me about yourself":
                                1. Start with your name
                                2. Education / current status
                                3. Skills and interests
                                4. Project / experience if applicable
                                5. Career goal
                                6. Natural ending

                                For "What are your strengths?":
                                1. 2-3 genuine strengths choose karo
                                2. Har strength ko briefly explain karo
                                3. Ek small example do
                                4. Strengths ko job se connect karo
                                5. Naturally end karo

                                For "What are your weaknesses?":
                                1. Ek genuine but manageable weakness choose karo
                                2. Us weakness ko briefly explain karo
                                3. Explain karo ki uska work par kya effect hua
                                4. Batao ki tum us weakness ko improve karne ke liye kya kar rahe ho
                                5. Positive improvement point ke saath answer end karo

                                For "Why should we hire you?":
                                1. Apni relevant skills mention karo
                                2. Learning/project/experience se example do
                                3. Batao ki role mein tum kya contribute kar sakte ho
                                4. Learning attitude show karo
                                5. Confidently end karo

                                For "Why do you want to join our company?":
                                1. Company/role mein tumhe kya interesting lagta hai, batao
                                2. Isse apne career interest se connect karo
                                3. Batao ki tum kya seekhna chahte ho
                                4. Explain karo ki ye role tumhare liye relevant kyun hai
                                5. Naturally end karo

                                For "Where do you see yourself in 5 years?":
                                1. Apni professional direction batao
                                2. Kaunsi skills develop karna chahte ho, batao
                                3. Realistic career growth mention karo
                                4. Learning aur responsibility lene ka attitude show karo
                                5. Positive way mein end karo

                                For "How do you handle pressure?":
                                1. Pressure ko handle karne ka apna approach batao
                                2. Tasks ko prioritize kaise karte ho, batao
                                3. Calm aur focused kaise rehte ho, explain karo
                                4. Agar applicable ho to small example do
                                5. Batao ki tumne kya seekha

                                For "Are you comfortable working in a team?":
                                1. Batao ki tum team mein comfortable ho ya nahi
                                2. Teammates ke saath communication kaise karte ho, batao
                                3. Teamwork mein tumhara role kya hota hai, mention karo
                                4. Agar applicable ho to small example do
                                5. Teamwork se kya seekha, explain karo

                                For "What are your career goals?":
                                1. Apna short-term goal batao
                                2. Kaunsi skills improve karna chahte ho, batao
                                3. Apni long-term direction mention karo
                                4. Explain karo ki job tumhe grow karne mein kaise help karegi
                                5. Naturally end karo

                                For "Do you have any questions for us?":
                                1. Role ke baare mein question poochho
                                2. Learning ya responsibilities ke baare mein poochho
                                3. Team/work environment ke baare mein relevant question poochh sakte ho
                                4. Aise questions avoid karo jinke answers already obvious hain
                                5. Politely end karo

                                IMPORTANT:
                                Upar diye gaye structures sirf examples hain.

                                Hamesha actual selected interview question ke according
                                sabse suitable structure choose karo.

                                ============================================================
                                IMPORTANT POINTS
                                ============================================================

                                4 se 6 short aur practical points do.

                                • Naturally speak karne ki advice do.
                                • Answer ko word-by-word memorize mat karne bolo.
                                • Answer ko question par focused rakho.
                                • Simple English use karo.
                                • Difficult vocabulary avoid karo.
                                • Corporate language avoid karo.
                                • Unnecessary personal information mat do.
                                • Jab appropriate ho, answer ko around 45-60 seconds rakho.
                                • Honest aur realistic answer do.

                                ============================================================
                                SAMPLE ANSWER
                                ============================================================

                                Ek natural spoken answer likho jo ek college student ya fresher
                                real interview mein actually bol sake.

                                IMPORTANT:

                                • SAMPLE ANSWER ko directly is question ka answer dena chahiye:
                                "{selected_question}"

                                • "Tell me about yourself" wala structure doosre questions ke
                                liye use MAT karo.

                                • Name, education, project ya career goal tabhi add karo jab
                                selected question ke liye actually relevant ho.

                                • Short aur natural sentences use karo.

                                • Answer real student ke speaking style jaisa lagna chahiye.

                                • Answer textbook jaisa nahi lagna chahiye.

                                • Answer corporate speech jaisa nahi lagna chahiye.

                                • In phrases ko use MAT karo:
                                "add value to the organization"
                                "professional journey"
                                "dynamic environment"
                                "leverage my skills"
                                "contribute to the growth of the organization"

                                • Personal information invent MAT karo.

                                • College, degree, company, job, internship, project ya
                                experience invent MAT karo.

                                • Agar example ki zarurat ho aur personal information available
                                nahi hai, to simple generic example use karo ya explain karo
                                ki student ko kya mention karna chahiye.

                                • Candidate ko experienced professional jaisa mat dikhao agar
                                wo fresher hai.

                                • Answer realistic aur bolne mein easy hona chahiye.

                                IMPORTANT LANGUAGE RULE:

                                HOW TO ANSWER aur IMPORTANT POINTS:
                                → Hinglish mein explanation do.

                                SAMPLE ANSWER:
                                → Simple, natural English mein answer do,
                                kyunki student actual English HR interview ki practice kar raha hai.

                                ============================================================
                                FINAL CHECK
                                ============================================================

                                Answer dene se pehle check karo:

                                1. Kya HOW TO ANSWER selected question ke according hai?
                                2. Kya SAMPLE ANSWER directly selected question ka answer hai?
                                3. Kya answer natural aur bolne mein easy hai?
                                4. Kya koi personal information invent nahi ki gayi?
                                5. Kya corporate/tough language avoid ki gayi hai?
                                6. Kya har question ke liye same structure use nahi hua?

                                Do not add any extra sections.
                                """

                                # -------------------------------------------------
                                # OPENROUTER API CALL
                                # -------------------------------------------------

                                try:

                                    response = openrouter_client.chat.completions.create(
                                        model="openrouter/free",
                                        messages=[
                                            {
                                                "role": "user",
                                                "content": prompt
                                            }
                                        ]
                                    )

                                    print("\n")
                        

                                    print("\n")
                                    print(response.choices[0].message.content)

                                except Exception as e:

                                    print("\n")
                                    print("=" * 60)
                                    print("OPENROUTER ERROR")
                                    print("=" * 60)

                                    print("\n", e)

                            else:

                                print("\nInvalid choice.")

                                
                                        
                        elif c=="10":
                            break
                        else:
                            print("Choose a valid option.")             
                else:
                    print("NOT REGISTER.")

                
        else:
            print("INVALID CHOICE")  

            #admin login       
    elif ti=="2":
        nv= input("ENTER YOUR NAME = ")
        pss = input("ENTER YOUR PASSWORD (if you lost your password press 3 )= ")

        if pss =="3":
            print("SECURITY QUESTIONS")
            p= (input("WHAT IS YOUR SECURITY ANSWER = "))
            sql = """
            SELECT * FROM Admin
            WHERE Name = %s AND secu_ans = %s
            """

            data = (nv, p)

            cursor.execute(sql, data)
            result = cursor.fetchone()
            if result:
                                
                    print("IF YOU CHECK YOUR DETAILS CLICK 1.")
                    
                    c=input("ENTER YOUR CHOICE = ")
                    if c=="1":
                        print("=" * 38)
                        print("       YOUR DETAIL IS")
                        sql="""
                        select Name, Email, set_pss from admin
                        where name = %s
                        """           
                        data = (nv,)
                        cursor.execute(sql,data)
                        ec=cursor.fetchall()
                        for row in ec:
                            print("=" * 38)
                            
                            print("| Name         :",row[0])
                            print("| Email        :",row[1])
                            print("| Password     :",row[2])

                                                                                                          
                    else:
                        print("not valid choice")
                
            else:
                print("WRONG NAME OR SECURITY ANSWER.")
        else:
            sql = """
            SELECT * FROM Admin
            WHERE Name = %s AND set_pss = %s
            """

            data = (nv, pss)

            cursor.execute(sql, data)
            result = cursor.fetchone()
            if result:
                print("LOGIN SUCCESSFULLY.")
                while True:
                    print("=" * 34)
                    print("\n 1.Check Student Data. \n 2.Check Results. \n 3.Add Announcement. \n 4.View Announcement. \n 5.Show all feedback. \n 6.Exit")
                    c=int(input("What Want You Check?? : "))
                    match c:
                        case 1:
                            print("\n ============================== \n")
                            sql="select * from students"
                            cursor.execute(sql)
                            ec = cursor.fetchall()
                            print("================================")
                            
                            print("\n STUDENT RECORDS \n\n")
                            print(f"|  {'Student Id':<12}| {'Name':<20}| {'Email':<31}| {'Password':<15}| {'Roll Number':<15}| {'College Name':<20}| {'Course':<15}| {'Security Answer':<20}| {'Subject':<15}| {'Branch':<15}|")
                            print("-"*185)
                            for row in ec:    
                                print(f"|  {str(row[0]):<12}| {str(row[1]):<20}| {str(row[2]):<31}| {str(row[3]):<15}| {str(row[4]):<15}| {str(row[5]):<20}| {str(row[6]):<15}| {str(row[7]):<20}| {str(row[8]):<15}| {str(row[10]):<15}| ")
                            ########## delete student option
                            print("\n1. Delete Student")
                            print("2. Back")

                            choice = int(input("Enter your choice: "))

                            if choice == 1:

                                student_id = int(input("Enter Student ID to delete: "))

                                sql = "DELETE FROM students WHERE student_id = %s"
                                cursor.execute(sql, (student_id,))

                                
                                con.commit()

                                if cursor.rowcount > 0:
                                    print("Student Deleted Successfully!")
                                else:
                                    print("Student ID Not Found!")

                            elif choice == 2:
                                print("Going Back...")                                

                        case 2:
                            print("============================== \n STUDENTS RESULT RECORD.")
                            sql="select * from result"
                            cursor.execute(sql)
                            ec = cursor.fetchall()
                            print("============================== \n")
                            print(f"|  {'Result ID':<12}| {'Student ID':<12}| {'Name':<20}| {'Subject':<20}| {'Total Questions':<12}| {'Score':<12}| {'Percentage':<12}| {'Time Taken':<12}| {'Status':<15}| {'Medium':<20}")
                            print("-"*185)
                            for row in ec:
                                print(f"|  {str(row[0]):<12}| {str(row[1]):<12}| {str(row[9]):<20}| {str(row[2]):<20}| {str(row[3]):<12}   | {str(row[4]):<12}| {str(row[5]):<12}| {str(row[6]):<12}| {str(row[7]):<15}| {str(row[8]):<20}")
                        
                        case 3:
                            print("========== ADD ANNOUNCEMENT ==========")
                            title = input("ENTER ANNOUNCEMENT TITLE = ")
                            message = input("ENTER ANNOUNCEMENT MESSAGE = ")
                            date = (input("ENTER ANNOUNCEMENT DATE = "))
                            sql="""
                            insert into announce
                            (title, message, announce_date)
                            values(%s, %s, %s)
                            """
                            data = (title, message, date)
                            cursor.execute(sql, data)
                            con.commit()
                            print("ANNOUNCEMENT ADDED SUCCESSFULLY.")                           
                        case 4:
                            
                            sql = """
                            select * from announce
                            """
                            cursor.execute(sql)
                            ac = cursor.fetchall()
                            print("\n")
                            if ac:
                                print("========== ANNOUNCEMETS ==========")
                                for row in ac:
                                    print("Announcement ID : ",row[0])
                                    print("Title           : ",row[1])
                                    print("Message         : ",row[2])
                                    print("Date            : ",row[3])
                                    print("Status          : ",row[4])
                                    print("=" * 34) 
                                   
                                    
                                print("\n1.DELETE ANNOUNCEMENT.")
                                print("2.INACTIVE ANNOUNCEMENT.")
                                print("3.ACTIVE ANNOUNCEMENT.")
                                print("4.GOING BACK.")
                                
                                
                                ch = int(input("ENTER YOUR CHOICE = "))
                                if ch == 1:
                                    ann_id = int(input("ENTER ANNOUNCEMENT ID = "))
                                    sql = "DELETE FROM announce where ann_id = %s"
                                    cursor.execute(sql, (ann_id,))
                                    con.commit()
                                    if cursor.rowcount>0:
                                        print("DELETED SUCCESSFULLY.")
                                    else:
                                        print("ID NOT FOUND !!!")         

                                elif ch == 2:
                                    ann_id = int(input("ENTER ANNOUNCEMENT ID = "))
                                    sql="""
                                    update announce SET status = 'INACTIVE' where ann_id =%s
                                    """
                                    cursor.execute(sql, (ann_id,))
                                    con.commit()
                                    if cursor.rowcount>0:
                                        print("ANNOUNCEMENT IS INACTIVE.")
                                    else:
                                        print("ID NOT FOUND")    
                                        
                                elif ch == 3:
                                    ann_id = int(input("ENTER ANNOUNCEMENT ID = "))
                                    sql="""
                                    update announce SET status = 'ACTIVE' where ann_id =%s
                                    """
                                    cursor.execute(sql, (ann_id,))
                                    con.commit()
                                    if cursor.rowcount>0:
                                        print("ANNOUNCEMENT IS ACTIVE.")
                                    else:
                                        print("ID NOT FOUND")        
                                    
                                elif ch == 4:
                                    print("GOING BACK......")
                                    
                                    
                                         
                                else:
                                    print("wrong choice.")    
                                    
                            else:
                                print("NO ANNOUCEMENTS.")  
                                
                                
                                
                        case 5:
                            sql = """
                            select * from feedback
                            """
                            cursor.execute(sql)
                            z = cursor.fetchall()
                            if z:
                                print("\n")
                                print("========== FEEDBACK ==========")
                                for row in z:
                                    print("Feedback ID : ",row[0])
                                    print("Student ID  : ",row[1]) 
                                    print("Name        : ",row[2])
                                    print("Feedback    : ",row[3])
                                    print("=" * 34)           
                                        
                        case 6:
                            print("Exiting Admin Panel...")
                            break       
                                
                            
                            
                            
                            
            else:
                print("INVALID.")
    else:
        print("INVALID.")            



