import json

from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify, flash
import mysql.connector
import cv2
from PIL import Image
import numpy as np
import os
import time
from datetime import date, datetime
import re
import threading


app = Flask(__name__)
app.secret_key = 'your secret key'

cnt = 0
pause_cnt = 0
justscanned = False

user = "iqmlhvyyatv7qono"
password = "jj36lbg9mfaucuee"
host = "dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
port = 3306
database = "vd2o5djn3ce6mnds"

mydb = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=zagusopas,
    port=port

)
#mycursor = mydb.cursor()
mycursor = mydb.cursor(buffered=True)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generate dataset >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def generate_dataset(nbr):
    face_classifier = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")

    mycursor.execute("select * from img_dataset WHERE img_person='" + str(nbr) + "'")
    data1 = mycursor.fetchall()
    for item in data1:
        imagePath = "dataset/" + nbr + "." + str(item[0]) + ".jpg"
        #print(imagePath)
        try:
            os.remove(imagePath)
        except:
            pass
    mycursor.execute("delete from img_dataset WHERE img_person='" + str(nbr) + "'")
    mydb.commit()

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor=1.3
        # Minimum neighbor = 5

        if faces is ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face

    cap = cv2.VideoCapture(0)

    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]

    img_id = lastid
    max_imgid = img_id + 100
    count_img = 0

    while True:
        ret, img = cap.read()
        if face_cropped(img) is None:
           frame1 = cv2.resize(img, (200, 200))
           frame1 = cv2.imencode('.jpg', frame1)[1].tobytes()
           yield (b'--frame1\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')
        if face_cropped(img) is not None:
            count_img += 1
            img_id += 1
            face = cv2.resize(face_cropped(img), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = "dataset/" + nbr + "." + str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count_img), (5, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

            mycursor.execute("""INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES
                                ('{}', '{}')""".format(img_id, nbr))
            mydb.commit()
            if int(img_id) == int(max_imgid):
                cv2.putText(face, "Train Complete", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(face, "Click Train Button.", (5, 45), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 255, 255), 1)
            frame = cv2.imencode('.jpg', face)[1].tobytes()
            yield (b'--frame1\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            if cv2.waitKey(1) == 13 or int(img_id) == int(max_imgid):
                break
                cap.release()
                cv2.destroyAllWindows()


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Train Classifier >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/train_classifier/<nbr>')
def train_classifier(nbr):
    user_id = session.get('user_id')  # Get the user's ID from the session
    #dataset_dir = "C:/Users/jd/PycharmProjects/FlaskOpencv_FaceRecognition/dataset"
    if not has_completed_training(user_id):
        dataset_dir = "dataset"

        path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L');
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split(".")[1])

            faces.append(imageNp)
            ids.append(id)
        ids = np.array(ids)

        # Train the classifier and save
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")


        mycursor.execute("UPDATE users SET completed_training = 1 WHERE id = %s", (user_id,))
        mydb.commit()

        flash('Training completed successfully.', 'success')
    else:
        flash('You can only train once.', 'warning')

    return redirect('/updateownprofile')

@app.route('/gendataset')
def gendataset():
    user_id = session['user_id']
    user_completed_process = get_user_training_status(user_id)
    return render_template('gendataset.html', user_completed_process=user_completed_process)

def has_completed_training(user_id):
    # Implement your logic to check if the user has completed training
    # For example, you can check the value of the 'completed_training' field in the database
    mycursor.execute("SELECT completed_training FROM users WHERE id = %s", (user_id,))
    result = mycursor.fetchone()

    if result and result[0] == 1:
        return True
    else:
        return False

def face_show():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        global justscanned
        global pause_cnt

        pause_cnt += 1

        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 70 and not justscanned:
                global cnt
                cnt += 1

                n = (100 / 30) * cnt
                # w_filled = (n / 100) * w
                w_filled = (cnt / 30) * w

                #cv2.rectangle(img, (x, y + h + 40), (x + w, y + h + 50), color, 2)
                #cv2.rectangle(img, (x, y + h + 40), (x + int(w_filled), y + h + 50), (153, 255, 255), cv2.FILLED)

            else:
                if not justscanned:
                    cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

            coords = [x, y, w, h]
        return coords

    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def face_recognition(group_id, attendancetime, attendanceduration, random_attendance_id, user_id):
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        global justscanned
        global pause_cnt

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        pause_cnt += 1

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 80 and not justscanned:
                global cnt
                cnt += 1

                if int(cnt) == 30:
                    cnt = 0
                    atime = str(date.today()) + ' ' + str(attendancetime) + ':00'

                    mycursor.execute("select a.img_person, b.first_name, b.last_name "
                                     "  from img_dataset a "
                                     "  left join users b on a.img_person = b.id "
                                     " where a.img_id = " + str(id))
                    row = mycursor.fetchone()
                    pnbr = row[0]
                    pname = row[1]
                    pskill = row[2]

                    mycursor.execute("select count(*) "
                                     "  from accs_hist "
                                     " where accs_date = curdate() AND group_id = '" + str(group_id) + "' AND accs_prsn = '" + pnbr + "' AND random_attendance_id = '" + str(random_attendance_id) + "'")
                    row = mycursor.fetchone()
                    rowcount = row[0]

                    if rowcount > 0:
                        cv2.putText(img, pname + ', You already marked your attendance', (x - 10, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
                        justscanned = True
                        pause_cnt = 0
                    else:
                        cv2.putText(img, pname, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2,
                                    cv2.LINE_AA)

                        mycursor.execute("insert into accs_hist (accs_date, accs_prsn, group_id, accs_added, random_attendance_id) values('" + str(
                            date.today()) + "', '" + pnbr + "', '" + str(group_id) + "', '" + str(atime) + "', '" + str(
                            random_attendance_id) + "')")
                        mydb.commit()

                        time.sleep(1)

                        justscanned = True
                        pause_cnt = 0
                else:
                    justscanned = False  # Moved this line here

            else:
                if not justscanned:
                    cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, 'You already marked your attendance', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

    def recognize(img, clf, faceCascade):
        draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break



# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< END Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Optimization >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< END  Optimization >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/vfdataset_page')
def vfdataset_page():
    return render_template('gendataset.html', prs=session['user_id'])


@app.route('/vidfeed_dataset/<nbr>')
def vidfeed_dataset(nbr):
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_dataset(nbr), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    random_attendance_id = session['random_attendance_id']
    mycursor.execute("select a.group_id, a.random_time, a.duration "
                     "  from random_attendance a "
                     " where a.id = " + str(random_attendance_id))
    row = mycursor.fetchone()

    group_id = row[0]
    attendancetime = row[1]
    attendanceduration = row[2]
    user_id = session['user_id']

    #attendancetime = session['attendancetime']
    #attendanceduration = session['attendanceduration']

    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_recognition(group_id, attendancetime, attendanceduration, random_attendance_id,user_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_show')
def video_show():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_show(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fr_page', methods=['GET', 'POST'])
def fr_page():
    """Video streaming home page."""
    user_id = session['user_id']
    data=""

    mycursor.execute("select a.accs_id, a.accs_prsn, b.first_name, b.last_name, a.accs_added "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id "
                     " where a.accs_prsn = '" + str(user_id) + "' AND a.accs_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()

    atdone = "no"
    random_attendance_id = session['random_attendance_id']
    mycursor.execute("select count(*) "
                     "  from accs_hist "
                     " where accs_date = curdate() AND  accs_prsn = '" + str(user_id) + "' AND random_attendance_id = '" + str(random_attendance_id) + "'")
    row = mycursor.fetchone()
    rowcount = row[0]
    if rowcount > 0:
        atdone = "yes"
    else:
        atdone = "no"
    '''
    attendancetime = str(date.today())
    if request.args.get('time') != "" and request.args.get('time') != None and request.args.get('time') != "auto":
        session['attendancetime'] = request.args.get('time')
        attendancetime = session['attendancetime']
        #attendancetime = request.args.get('time')

    session['attendanceduration'] = 0
    if request.args.get('duration') != "" and request.args.get('duration') != None and request.args.get('duration') != "auto":
        session['attendanceduration'] = request.args.get('duration')
    '''
    
    random_attendance_id = session['random_attendance_id']
    mycursor.execute("select a.group_id, a.random_time, a.duration "
                     "  from random_attendance a "
                     " where a.id = " + str(random_attendance_id))
    row = mycursor.fetchone()
    #group_id = row[0]
    #session['attendancetime'] = row[1]
    session['attendanceduration'] = row[2]

    #session['random_attendance_id']="6"
    return render_template('fr_page.html', data=data, data1=atdone)


@app.route('/countTodayScan')
def countTodayScan():
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="zagusopas"
  )
  mycursor = mydb.cursor()

  mycursor.execute("select count(*) "
                   "  from accs_hist "
                   " where accs_date = curdate() ")
  row = mycursor.fetchone()
  rowcount = row[0]
  print(rowcount)
  return jsonify({'rowcount': rowcount})


@app.route('/loadData', methods=['GET', 'POST'])
def loadData():
  mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="zagusopas"
  )
  mycursor = mydb.cursor()
  user_id = session['user_id']

  mycursor.execute("select a.accs_id, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%H:%i:%s') "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id "
                     " where a.accs_date = curdate() and b.id = " + str(user_id) +
                     " order by 1 desc")

  '''
    mycursor.execute("select a.accs_id, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%H:%i:%s') "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id "
                     " where a.accs_date = curdate() "
                     " order by 1 desc")
  '''
  data = mycursor.fetchall()

  return jsonify(response=data)


@app.route('/')
def add_login_view():
  msg = ""
  return render_template('login.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login_submit():

    msg = ""
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #mycursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password,))
        mycursor.execute("SELECT * FROM users WHERE email ='%s' AND password ='%s'" % (email, password))
        account = mycursor.fetchone()
        if account:
            if account[7] != 'teacher':
                #if account[14] == 1:
                  session['loggedin'] = True
                  session['user_id'] = account[0]
                  session['user_name'] = account[1]
                  session['user_email'] = account[3]
                  session['user_role'] = account[7]
                  session['user_photo'] = account[13]
                  session['random_attendance_id'] = '0'
                  msg = "<div class='alert alert-success'>Successfully LogIn</div>"
                  #return render_template('updateownprofile.html', msg=msg)
                  return redirect(url_for('updateownprofile'))
                #else:
                    #msg = " Your account is not approved!"
            elif account[7] != 'admin':
                # if account[14] == 1:
                session['loggedin'] = True
                session['user_id'] = account[0]
                session['user_name'] = account[1]
                session['user_email'] = account[3]
                session['user_role'] = account[7]
                session['user_photo'] = account[13]
                session['random_attendance_id'] = '0'
                msg = "<div class='alert alert-success'>Successfully LogIn</div>"
                # return render_template('updateownprofile.html', msg=msg)
                return redirect(url_for('updateownprofile'))
            # else:
            # msg = " Your account is not approved!"
            else:
                session['loggedin'] = True
                session['user_id'] = account[0]
                session['user_name'] = account[1]
                session['user_email'] = account[3]
                session['user_role'] = account[7]
                session['user_photo'] = account[13]
                msg = "Successfully LogIn"
                #return render_template('updateownprofile.html', msg=msg)
                return redirect(url_for('updateownprofile'))
        else:
            msg = """Your email or password is incorrect"""
    return render_template('login.html', msg=msg)

@app.route('/signup')
def signup():
  msg = "Signup Successful"
  return render_template('signup.html', msg=msg)

@app.route('/signup', methods=['POST'])
def signup_submit():
    msg = ""
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'password' in request.form and 'email' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        re_password = request.form['re_password']
        email = request.form['email']
        user_role = "student"
        phone = ""

        if password == re_password:
           mycursor.execute("SELECT * FROM users WHERE email = '%s'" % (email))
           account = mycursor.fetchone()
           if account:
              msg = 'Account already exists !'
           elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
              msg = 'Invalid email address !'
           elif not re.match(r'[A-Za-z0-9]+', first_name):
              msg = 'Username must contain only characters and numbers !'
           elif not first_name or not password or not email:
              msg = 'Please fill out the form !'
           else:
              photo = request.form['photo']
              if request.files:
                   image = request.files["fileToUpload"]
                   if image.filename != '' and image.filename != None:
                       image.filename = first_name + "-" + image.filename
                       image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                       photo = image.filename
              else:
                   photo = request.form['photo']

              mycursor.execute("insert into users ( first_name, last_name, email, password, user_role, phone, photo) values('" + str(
                  first_name) + "', '" + str(last_name) + "', '" + str(email) + "', '" + str(password) + "', '" + str(user_role) + "', '" + str(phone) + "', '" + str(
                          photo) + "')")
              mydb.commit()

              msg = 'You have successfully registered !'
              return add_login_view()
        else:
           msg = ' Your password and re-entered password is not matching.'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)

@app.route('/updateownprofile')
def updateownprofile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        mycursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
        account = mycursor.fetchone()
        # Show the profile page with account info
        return render_template('updateownprofile.html', account=account)
    else:
        return redirect(url_for('login'))



#app.config["IMAGE_UPLOADS"] = "C:/Users/raja/PycharmProjects/FlaskOpencv_FaceRecognition/static/user_photo/"
app.config["IMAGE_UPLOADS"] = "static/user_photo"

@app.route('/updateownprofile', methods=['GET', 'POST'])
def updateownprofile_submit():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        i_d = request.form['i_d']
        userlist_id = session['user_id']
        photo = request.form['photo']
        if request.files:
            image = request.files["fileToUpload"]
            if image.filename != '' and image.filename != None:
               image.filename = first_name + "-" + image.filename
               image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
               photo = image.filename
               session['user_photo'] = photo
            #return render_template("updateownprofile.html", uploaded_image=image.filename)
            #return updateownprofile()
        else:
            photo = request.form['photo']

        mycursor.execute("UPDATE users SET first_name='" + str(first_name) + "',last_name='" + str(last_name) + "',email='" + str(email) + "',phone='" + str(phone) + "', photo='" + str(photo) + "', address_line1='" + str(address_line1) + "', address_line2='" + str(address_line2) + "', dob='" + str(dob) + "', i_d='" + str(i_d) + "' WHERE id='" + str(userlist_id) + "'")
        mydb.commit()

    #return render_template("updateownprofile.html")
    return updateownprofile()

@app.route('/userlist')
def userlist():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="zagusopas"
    )
    mycursor = mydb.cursor()
    data1 = ""
    #mycursor.execute("select * from users where user_role!='teacher'")
    mycursor.execute("SELECT DISTINCT(b.img_person), a.* FROM users a LEFT JOIN img_dataset b ON a.id = b.img_person WHERE user_role NOT IN ('teacher', 'admin')")
    data = mycursor.fetchall()
    creater_id = session['user_id']
    mycursor.execute("select * from groups WHERE creater_id='" + str(creater_id) + "'")
    data1 = mycursor.fetchall()
    mycursor.execute("select * from join_groups")
    data2 = mycursor.fetchall()
    #return jsonify(response=data)
    #return render_template('userlist.html')
    return render_template('userlist.html', data=data, data1=data1, data2=data2)



@app.route('/user_functions', methods=['GET', 'POST'])
def user_functions():
    userlistid = request.args.get('userlistid')
    action = request.args.get('action')
    if action == 'approved':
        mycursor.execute("UPDATE users SET approved='1' WHERE id='" + str(userlistid) + "'")
        mydb.commit()
    #return userlist()
    return redirect(url_for('userlist'))



@app.route('/group_functions', methods=['GET', 'POST'])
def group_functions():
    userlistid = request.args.get('userlistid')
    group_id = request.args.get('group_id')
    action = request.args.get('action')
    if action == 'invite':
        mycursor.execute("SELECT * FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlistid) + "'")
        account = mycursor.fetchone()
        if account:
            msg=""
        else:
            mycursor.execute("INSERT INTO join_groups ( group_id, user_id) VALUES ('" + str(group_id) + "','" + str(userlistid) + "')")
            mydb.commit()
        return redirect(url_for('userlist'))

    if action == 'approved':
        mycursor.execute("UPDATE join_groups SET user_approved='1' WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlistid) + "'")
        mydb.commit()
        #return userlist()
        return redirect(url_for('grouplist'))

    if request.method == "POST":
        group_id = request.form['select_group']
        print(group_id)
        #print(request.form.getlist('userlist[]'))
        for userlistid in request.form.getlist('userlist[]'):
            mycursor.execute("SELECT * FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(
                userlistid) + "'")
            account = mycursor.fetchone()
            if account:
                msg = ""
            else:
                mycursor.execute("INSERT INTO join_groups ( group_id, user_id) VALUES ('" + str(group_id) + "','" + str(
                    userlistid) + "')")
                mydb.commit()
            print(userlistid)

        #return render_template('userlist.html', msg=userlist)
        return redirect(url_for('userlist'))


@app.route('/grouprequest', methods=['GET', 'POST'])
def grouprequest():
    if 'loggedin' in session:
        m=""
    else:
        return redirect(url_for('login'))

    group_id = request.args.get('group_id')
    action = request.args.get('action')
    groupteacher = request.args.get('groupteacher')
    groupname = request.args.get('groupname')
    msg = "yes"
    userrole = session['user_role']
    if action == 'invitelink' and userrole != 'teacher':
        userlistid = session['user_id']

        mycursor.execute(
            "SELECT * FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlistid) + "'")
        account = mycursor.fetchone()
        if account:
            mycursor.execute(
                "SELECT * FROM join_groups WHERE user_approved = 0 AND group_id='" + str(group_id) + "' AND user_id='" + str(
                    userlistid) + "'")
            accounts = mycursor.fetchone()
            if accounts:
                #return render_template("grouprequest.html", group_id=group_id,groupteacher=groupteacher,groupname=groupname)
                msg = "Please accept the request."
            else:
                msg = "You already a member of this group."
                return redirect(url_for('grouplist'))
        else:
            mycursor.execute("INSERT INTO join_groups ( group_id, user_id) VALUES ('" + str(group_id) + "','" + str(
                userlistid) + "')")
            mydb.commit()
            msg = "inserted"
        #return render_template("grouprequest.html", group_id=group_id,groupteacher=groupteacher,groupname=groupname)

    if request.method == "POST" and 'accept' in request.form:
        joinrequest = request.form['accept']
        print(joinrequest)
        userlistid = session['user_id']
        mycursor.execute(
            "UPDATE join_groups SET user_approved='1' WHERE group_id='" + str(group_id) + "' AND user_id='" + str(
                userlistid) + "'")
        mydb.commit()
        # return userlist()
        return redirect(url_for('grouplist'))

    if request.method == "POST" and 'reject' in request.form:
        reject = request.form['reject']
        print(reject)
        return redirect(url_for('grouplist'))

    print(msg)
    if msg == "yes":
        return redirect(url_for('updateownprofile'))

    return render_template('grouprequest.html', msg=msg, group_id=group_id,groupteacher=groupteacher,groupname=groupname)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    #return redirect(url_for('login'))
    return login_submit()

@app.route('/groups')
def groups():
    creater_id = session['user_id']
    mycursor.execute("select id, group_name, date_format(created, '%d-%m-%Y %W %H:%i:%s') from groups where creater_id='" + str(
            creater_id) + "'")
    data = mycursor.fetchall()
    return render_template('groups.html', data=data)

@app.route('/groups', methods=['POST'])
def groups_submit():
    if request.method == "POST":
        group_name = request.form['group_name']
        creater_id = session['user_id']
        mycursor.execute("INSERT INTO groups ( group_name, creater_id) VALUES ('" + str(group_name) + "','" + str(creater_id) + "')")
        mydb.commit()
    return redirect(url_for('groups'))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    id = request.args.get('id')
    tname = request.args.get('tname')
    rurl = request.args.get('rurl')
    mycursor.execute("DELETE FROM " + str(tname) + " WHERE id='" + str(id) + "'")
    mydb.commit()
    return redirect(url_for(rurl))

@app.route('/grouplist', methods=['GET', 'POST'])
def grouplist():
    user_id = session['user_id']
    action = request.args.get('action')
    group_id = request.args.get('group_id')
    if action == 'remove':
        mycursor.execute("DELETE FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(user_id) + "'")
        mydb.commit()

    #mycursor.execute("SELECT join_groups.group_id,groups.group_name,join_groups.user_approved FROM join_groups left JOIN groups ON join_groups.group_id=groups.id WHERE user_id='" + str(user_id) + "'")
    mycursor.execute("SELECT join_groups.group_id,groups.group_name,join_groups.user_approved,users.first_name,users.last_name FROM join_groups left JOIN groups ON join_groups.group_id=groups.id left JOIN users ON groups.creater_id=users.id WHERE user_id='" + str(
            user_id) + "'")
    data = mycursor.fetchall()

    group_id = request.args.get('group_id')
    groupteacher = request.args.get('groupteacher')
    groupname = request.args.get('groupname')
    action = request.args.get('action')
    data1 = ""
    if action == 'view_members':
        #mycursor.execute(
          #  "SELECT users.first_name,users.last_name,users.user_role FROM `join_groups` left JOIN groups ON join_groups.group_id=groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.user_approved='1' AND join_groups.group_id='" + str(
           #     group_id) + "'")
        mycursor.execute(
            "SELECT users.first_name,users.last_name,users.user_role FROM `join_groups` left JOIN groups ON join_groups.group_id=groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.group_id='" + str(
                group_id) + "'")
        data1 = mycursor.fetchall()
    return render_template('grouplist.html', data=data, data1=data1, groupteacher=groupteacher, groupname=groupname)

@app.route('/teachersignup')
def teachersignup():
  msg = ""
  return render_template('teachersignup.html', msg=msg)

@app.route('/teachersignup', methods=['POST'])
def teachersignup_submit():
    msg = ""
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'password' in request.form and 'email' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        re_password = request.form['re_password']
        email = request.form['email']
        user_role = "teacher"
        phone = ""

        if password == re_password:
           mycursor.execute("SELECT * FROM users WHERE email = '%s'" % (email))
           account = mycursor.fetchone()
           if account:
              msg = 'Account already exists !'
           elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
              msg = 'Invalid email address !'
           elif not re.match(r'[A-Za-z0-9]+', first_name):
              msg = 'Username must contain only characters and numbers !'
           elif not first_name or not password or not email:
              msg = 'Please fill out the form !'
           else:
              mycursor.execute("insert into users ( first_name, last_name, email, password, user_role, phone) values('" + str(
                  first_name) + "', '" + str(last_name) + "', '" + str(email) + "', '" + str(password) + "', '" + str(user_role) + "', '" + str(phone) + "')")
              mydb.commit()
              msg = 'You have successfully registered !'
              return add_login_view()
        else:
           msg = ' Your password and re-entered password is not matching.'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('teachersignup.html', msg=msg)


@app.route('/report', methods=['GET', 'POST'])
def report():
    user_id = session['user_id']
    user_role = session['user_role']
    filters = ""
    if request.method == 'POST' and 'filter' in request.form and 'startdate' in request.form and 'enddate' in request.form:
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        if request.form['startdate'] != "" and request.form['enddate'] != "":
           filters = " and a.accs_date BETWEEN '" + str(startdate) + "' AND '" + str(enddate) + "'"

    if request.method == 'POST' and 'filter' in request.form and 'group' in request.form:
        if request.form['group'] != "":
            group = request.form['group']
            filters += " and c.group_name LIKE '%" + str(group) + "%'"
    print(filters)
    if user_role != 'teacher':
        mycursor.execute(
            "select c.group_name, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%d-%m-%Y %W %H:%i:%s') "
            "  from accs_hist a "
            "  left join users b on a.accs_prsn = b.id "
            "  left join groups c on a.group_id = c.id "
            " where b.id = " + str(user_id) +
            "" + str(filters) +
            " order by a.accs_id desc")
    else:
        mycursor.execute(
            "select c.group_name, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%d-%m-%Y %W %H:%i:%s') "
            "  from accs_hist a "
            "  left join users b on a.accs_prsn = b.id "
            "  left join groups c on a.group_id = c.id "
            " where b.id != 0"
            "" + str(filters) +
            " order by a.accs_id desc")

    data = mycursor.fetchall()
    return render_template('report.html', data=data)

@app.route('/agrouplist', methods=['GET', 'POST'])
def agrouplist():

    group_id = request.args.get('group_id')
    groupteacher = request.args.get('groupteacher')
    groupname = request.args.get('groupname')
    action = request.args.get('action')
    data1 = ""
    data = ""
    data2 = ""
    if action == 'view_members':
        session['group_id'] = group_id
        session['groupteacher'] = groupteacher
        session['groupname'] = groupname
        session['actions'] = action

    if action == 'remove':
        userlist_id = request.args.get('userlist_id')
        mycursor.execute("DELETE FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlist_id) + "'")
        mydb.commit()

    if action == 'invite':
        userlist_id = request.args.get('userlist_id')
        mycursor.execute(
            "SELECT * FROM join_groups WHERE group_id='" + str(group_id) + "' AND user_id='" + str(userlist_id) + "'")
        account = mycursor.fetchone()
        if account:
            msg = ""
        else:
            mycursor.execute("INSERT INTO join_groups ( group_id, user_id) VALUES ('" + str(group_id) + "','" + str(
                userlist_id) + "')")
            mydb.commit()

    if session['actions'] == 'view_members':
        group_id = session['group_id']
        groupteacher = session['groupteacher']
        groupname = session['groupname']
        #mycursor.execute(
         #   "SELECT users.first_name,users.last_name,users.user_role,users.id,users.photo FROM `join_groups` left JOIN groups ON join_groups.group_id=groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.user_approved='1' AND join_groups.group_id='" + str(
           #     group_id) + "'")
        mycursor.execute(
            "SELECT users.first_name,users.last_name,users.user_role,users.id,users.photo FROM `join_groups` left JOIN groups ON join_groups.group_id=groups.id left JOIN users ON join_groups.user_id=users.id WHERE join_groups.group_id='" + str(
                group_id) + "'")
        data1 = mycursor.fetchall()
        mycursor.execute("select * from users where user_role!='teacher'")
        data2 = mycursor.fetchall()

    if action == 'view_report':
        userlist_id = request.args.get('userlist_id')
        mycursor.execute(
            "select a.accs_id, a.accs_prsn, b.first_name, b.last_name, date_format(a.accs_added, '%d-%m-%Y %W %H:%i:%s') "
            "  from accs_hist a "
            "  left join users b on a.accs_prsn = b.id "
            " where b.id = " + str(userlist_id) +
            " and a.group_id = '" + str(group_id) + "'"
            " order by a.accs_id desc")
        data = mycursor.fetchall()

    user_id = session['user_id']
    mycursor.execute(
        "select * from random_attendance where DATE(created)=CURDATE() AND TIME_FORMAT(random_time, '%H:%i')>=TIME_FORMAT(CURRENT_TIME(), '%H:%i') AND group_id='" + str(group_id) + "' AND user_id='" + str(user_id) + "'")
    data3 = mycursor.fetchall()

    mycursor.execute(
        "select *,now() from random_attendance where DATE(created)=CURDATE() AND TIME_FORMAT(random_time, '%H:%i')<TIME_FORMAT(CURRENT_TIME(), '%H:%i') AND group_id='" + str(
            group_id) + "' AND user_id='" + str(user_id) + "'")
    data4 = mycursor.fetchall()

    return render_template('agrouplist.html', data=data, data1=data1, groupteacher=groupteacher, groupname=groupname, group_id=group_id, data2=data2, data3=data3, data4=data4)

@app.route('/loadattendanceData', methods=['GET', 'POST'])
def loadattendanceData():

  group_id = session['group_id']
  mycursor.execute(
            "select COUNT(a.accs_prsn) as v, b.first_name, b.last_name,a.accs_prsn from accs_hist a left join users b on a.accs_prsn = b.id where a.group_id = '" + str(group_id) + "' GROUP BY a.accs_prsn")
  data = mycursor.fetchall()

  return jsonify(response=data)

@app.route('/loadattendanceDatareport', methods=['GET', 'POST'])
def loadattendanceDatareport():
  user_id = session['user_id']
  user_role = session['user_role']
  #group_id = session['group_id']
  if user_role != 'teacher':
      mycursor.execute(
          "select COUNT(a.accs_prsn) as v, c.group_name, b.first_name, b.last_name,a.accs_prsn,a.group_id from accs_hist a left join users b on a.accs_prsn = b.id left join groups c on a.group_id=c.id WHERE a.accs_prsn='" + str(user_id) + "' GROUP BY a.group_id")
  else:
      mycursor.execute(
            "select COUNT(a.accs_prsn) as v, b.first_name, b.last_name,a.accs_prsn from accs_hist a left join users b on a.accs_prsn = b.id GROUP BY a.accs_prsn")

  data = mycursor.fetchall()

  return jsonify(response=data)



@app.route('/setrandomattendance', methods=['GET', 'POST'])
def setrandomattendance():
   if request.method == "POST":
       group_id = request.form['group_id']
       duration = request.form['duration']
       user_id = session['user_id']
       status = "active"
       #random_time = str(request.form.getlist['random_time[]'])
       for random_time in request.form.getlist('random_time[]'):
           print(random_time)
           mycursor.execute(
               "INSERT INTO random_attendance ( user_id, group_id, random_time, duration, status) VALUES ('" + str(
                   user_id) + "','" + str(
                   group_id) + "','" + str(random_time) + "','" + str(duration) + "','" + str(status) + "')")
           mydb.commit()
       print(random_time)

   data = ""
   #return jsonify(response=data)
   return redirect(url_for('agrouplist'))


@app.route('/countTodayAttenScan', methods=['GET', 'POST'])
def countTodayAttenScan():
    user_id = session['user_id']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="zagusopas"
    )
    #mycursor = mydb.cursor()
    mycursor = mydb.cursor(buffered=True)
    #mycursor.execute("select a.group_id,a.random_time,now(),CURRENT_TIME() from random_attendance a left join join_groups c on a.group_id=c.group_id WHERE c.user_id='" + str(user_id) + "' AND DATE(a.created)=CURDATE() AND a.random_time>CURRENT_TIME()")
    #mycursor.execute("select a.id from random_attendance a left join join_groups c on a.group_id=c.group_id WHERE c.user_id='" + str(user_id) + "' AND DATE(a.created)=CURDATE() AND TIME_FORMAT(a.random_time, '%H:%i')=TIME_FORMAT(CURRENT_TIME(), '%H:%i')")
    mycursor.execute("select a.id from random_attendance a left join join_groups c on a.group_id=c.group_id WHERE c.user_id='" + str(
            user_id) + "' AND DATE(a.created)=CURDATE() AND TIME_FORMAT(a.random_time, '%H')=TIME_FORMAT(CURRENT_TIME(), '%H') AND TIME_FORMAT(CURRENT_TIME(), '%i') - TIME_FORMAT(a.random_time, '%i')<=2")
    row = mycursor.fetchone()
    print(row)
    random_attendance_id = ""
    if row:
        print("row")

        random_attendance_id = str(row[0])
        mycursor.execute(
            "select count(*) from accs_hist a WHERE a.accs_prsn='" + str(
                user_id) + "' AND a.random_attendance_id ='" + str(random_attendance_id) + "'")
        row1 = mycursor.fetchone()
        rowcount = row1[0]
        if rowcount>0:
            print("done already")
        else:
            session['random_attendance_id'] = random_attendance_id
    print(random_attendance_id)
    return jsonify({'random_attendance_id': random_attendance_id})



############################## User management routes #######################################

@app.route('/users')
def users():
    # Fetch and display the list of users from the database
    mycursor.execute("SELECT id, first_name, last_name, email, user_role, password FROM users")
    users = [{'id': user[0], 'first_name': user[1], 'last_name': user[2], 'email': user[3], 'user_role': user[4],
              'password': user[5]} for user in mycursor.fetchall()]
    return render_template('users.html', users=users)



@app.route('/add_user', methods=['POST'])
def add_user():
    # Add a new user to the database
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        user_role = request.form['user_role']
        password = request.form['password']

        # Check if the email is already used by another user
        mycursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = mycursor.fetchone()

        if existing_user:
            flash('Email already in use by another user.', 'error')
        elif not first_name or not last_name or not email or not user_role:
            flash('All fields are required.', 'error')
        else:
            mycursor.execute(
                "INSERT INTO users (first_name, last_name, email, user_role, password) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, email, user_role, password))
            mydb.commit()
            flash('User added successfully.', 'success')

    return redirect(url_for('users'))


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Edit an existing user's information
    mycursor.execute("SELECT id, first_name, last_name, email, user_role, password FROM users WHERE id = %s",
                     (user_id,))
    user = mycursor.fetchone()

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('users'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        user_role = request.form['user_role']
        password = request.form['password']

        # Check if the email is already used by another user (excluding the user being edited)
        mycursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, user_id))
        existing_user = mycursor.fetchone()

        if existing_user:
            flash('Email already in use by another user.', 'error')
        elif not first_name or not last_name or not email or not user_role or not password:
            flash('All fields are required.', 'error')
        else:
            mycursor.execute(
                "UPDATE users SET first_name = %s, last_name = %s, email = %s, user_role = %s, password = %s WHERE id = %s",
                (first_name, last_name, email, user_role, password, user_id))
            mydb.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Delete a user from the database
    mycursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mydb.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('users'))


@app.route('/updateprofile', methods=['GET'])
def updateprofile():
    userlist_id = ""
    if request.args.get('id') != "" and request.args.get('id') != None:
      session['userlist_id'] = request.args.get('id')
    userlist_id = session['userlist_id']
    mycursor.execute("SELECT * FROM users WHERE user_role!='teacher' AND id='" + str(userlist_id) + "'")
    account = mycursor.fetchone()
    # Show the profile page with account info
    return render_template('updateprofile.html', account=account)

@app.route('/updateprofile', methods=['POST'])
def updateprofile_submit():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        i_d = request.form['i_d']
        userlist_id = session['userlist_id']
        photo = request.form['photo']
        if request.files:
            image = request.files["fileToUpload"]
            if image.filename != '' and image.filename != None:
                image.filename = first_name + "-" + image.filename
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                photo = image.filename
            # return render_template("updateownprofile.html", uploaded_image=image.filename)
            # return updateownprofile()
        else:
            photo = request.form['photo']

        mycursor.execute("UPDATE users SET first_name='" + str(first_name) + "',last_name='" + str(last_name) + "',email='" + str(email) + "',phone='" + str(phone) + "', photo='" + str(photo) + "', address_line1='" + str(address_line1) + "', address_line2='" + str(address_line2) + "', dob='" + str(dob) + "', i_d='" + str(i_d) + "' WHERE id='" + str(userlist_id) + "'")
        mydb.commit()

    #return render_template("updateprofile.html")
    return updateprofile()


##################################### END USER MANAGEMENT#####################################################
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)



