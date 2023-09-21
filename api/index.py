from flask import Flask, render_template, request, redirect, url_for,session
from api.models import db, ToDo, User
from datetime import datetime


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.secret_key = '987123456abcd@@'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://oscar_user:12345@localhost/todo'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://default:8XUaQH9ijZbh@ep-old-dust-65584816-pooler.us-east-1.postgres.vercel-storage.com/verceldb'
db.init_app(app)

def date_conversion(date__time):
    if(date__time==''):
        return None
    else:
        date_time=date__time.replace("T"," ")
        datetime_object = datetime.strptime(date_time, '%Y-%m-%d')
        return datetime_object


@app.route('/')
def home():
    if 'user' in session:
        allTodo = ToDo.query.filter_by(owner=session['uid']).order_by(ToDo.sno.desc()).all()
        allTodo_dict=[]
        for i in allTodo:
            d={}
            d["sno"]=i.sno
            d["title"] = i.title
            d["description"] = i.description
            d["differ"] = i.differ
            d["status"] = i.status
            d["date_created"] = i.date_created
            d["date_deadline"] = i.date_deadline
            allTodo_dict.append(d)
        a=len(ToDo.query.filter_by(owner=session['uid'],status="On Progress").all())
        b=len(ToDo.query.filter_by(owner=session['uid'],status="Pending").all())
        c=len(ToDo.query.filter_by(owner=session['uid'],status="Completed").all())
        d=len(ToDo.query.filter_by(owner=session['uid'],status="Non-Prioritized").all())


        return render_template('index.html',allTodo=allTodo_dict,prog=a,pen=b,com=c,nop=d,uemail = session['user'])
    return redirect(url_for('login'))


@app.route('/newtask', methods=['GET', 'POST'])
def hello_world():
    if 'user' in session:
        if request.method == 'POST':
            title = request.form['title']
            desc = request.form['desc']
            differ = request.form['workdivision']
            status = request.form['Priority']

            date_deadline = request.form['finish']

            date_dead = date_conversion(date_deadline)
            # date_deadline=request.form['finish']

            # print(f"------------------------------------{type(date_deadline)}-------------------------,{date_deadline}")
            todo = ToDo(title=title, description=desc, differ=differ, status=status, date_deadline=date_dead,
                        owner=session['uid'])
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
    else:
        return redirect(url_for('login'))








@app.route('/pending')
def pending():
    if 'user' in session:
        alltodo = ToDo.query.filter_by(owner=session['uid'], status="Pending").order_by(ToDo.sno.desc()).all()
        allTodo_dict = []
        for i in alltodo:
            d = {}
            d["sno"] = i.sno
            d["title"] = i.title
            d["description"] = i.description
            d["differ"] = i.differ
            d["status"] = i.status
            d["date_created"] = i.date_created
            d["date_deadline"] = i.date_deadline
            allTodo_dict.append(d)
        return render_template('pending.html', allTodo=allTodo_dict,uemail = session['user'])

    else:
        return redirect(url_for('login'))


@app.route('/progress')
def progress():
    if 'user' in session:
        alltodo = ToDo.query.filter_by(owner=session['uid'], status="On Progress").order_by(ToDo.sno.desc()).all()
        allTodo_dict = []
        for i in alltodo:
            d = {}
            d["sno"] = i.sno
            d["title"] = i.title
            d["description"] = i.description
            d["differ"] = i.differ
            d["status"] = i.status
            d["date_created"] = i.date_created
            d["date_deadline"] = i.date_deadline
            allTodo_dict.append(d)
        return render_template('progess.html', allTodo=allTodo_dict,uemail = session['user'])
    else:
        return redirect(url_for('login'))



@app.route('/complete')
def complete():
    if 'user' in session:
        alltodo = ToDo.query.filter_by(owner=session['uid'], status="Completed").order_by(ToDo.sno.desc()).all()
        allTodo_dict = []
        for i in alltodo:
            d = {}
            d["sno"] = i.sno
            d["title"] = i.title
            d["description"] = i.description
            d["differ"] = i.differ
            d["status"] = i.status
            d["date_created"] = i.date_created
            d["date_deadline"] = i.date_deadline
            allTodo_dict.append(d)
        return render_template('complete.html', allTodo=allTodo_dict,uemail = session['user'])
    else:
        return redirect(url_for('login'))



@app.route('/nonpriority')
def nonpriority():
    if 'user' in session:
        alltodo = ToDo.query.filter_by(owner=session['uid'], status="Non-Prioritized").order_by(ToDo.sno.desc()).all()
        allTodo_dict = []
        for i in alltodo:
            d = {}
            d["sno"] = i.sno
            d["title"] = i.title
            d["description"] = i.description
            d["differ"] = i.differ
            d["status"] = i.status
            d["date_created"] = i.date_created
            d["date_deadline"] = i.date_deadline
            allTodo_dict.append(d)
        return render_template('nonpriority.html', allTodo=allTodo_dict,uemail = session['user'])

    else:
        return redirect(url_for('login'))


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if 'user' in session:
        if request.method == 'POST':
            sno = request.form['sno']
            title = request.form['title']
            desc = request.form['desc']
            differ = request.form['workdivision']
            status = request.form['Priority']
            date_deadline = request.form['finish']
            date_dead = date_conversion(date_deadline)

            todo = ToDo.query.filter_by(owner=session['uid'], sno=sno)
            todo.update({'sno': sno, 'title': title, 'description': desc, 'differ': differ, 'status': status,
                         'date_deadline': date_dead})
            db.session.commit()
            # return redirect("/",todo=todo)
            return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))




    # return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    if 'user' in session:
        todo = ToDo.query.filter_by(owner=session['uid'], sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    else:
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user',None)
        session.pop('uid', None)
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        u_nm = request.form['usernm']
        u_dob = request.form['dob']
        u_mail = request.form['umail']
        u_password = request.form['upass']

        dataflag_1 = User.query.filter_by(username=u_nm).first()
        dataflag_2 = User.query.filter_by(email=u_mail).first()

        if(dataflag_1 or dataflag_2):
            return render_template('signup.html',mesg="Usernbame or Email Exists Already Exists.")
        else:
            new_row = User(username=u_nm,email=u_mail,password=u_password,dob=u_dob)
            db.session.add(new_row)
            db.session.commit()
            return redirect(url_for('login'))

    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('signup.html',mesg="")

@app.route('/forgetpassword',methods=['GET','POST'])
def forget_password():
    if request.method == 'POST':
        u_dob = request.form['dob']
        u_mail = request.form['umail']
        u_password = request.form['upass']

        dataflag = User.query.filter_by(dob=u_dob,email=u_mail).first()




        if(dataflag):
            dataflag.password=u_password
            db.session.commit()
            return redirect(url_for('login'))

        else:
            return render_template('forget.html',mesg="DOB Or Email Doesn't Match")



    return render_template('forget.html',mesg="")





@app.route('/validuserdata',methods=['POST'])
def valid_user():
    if request.method == "POST":
        useremail= request.form['useremail']
        userpassword = request.form['userpassword']

        checkdata = User.query.filter_by(email=useremail,password=userpassword).first()


        if(checkdata):
            return '1'
        else:
            return '0'
    return '0'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        udata_email = request.form['uemail']
        udata_password = request.form['upassword']

        try:
            dbdata = User.query.filter_by(email=udata_email).first()
        except:
            dbdata = None

        if (dbdata) and (dbdata.password==udata_password):
            session['user'] = dbdata.username
            session['uid'] = dbdata.rid

            return redirect(url_for('home'))

        elif (dbdata) and(dbdata.password!=udata_password):
            return render_template('login.html',mesg="Failed Login | Password Wrong ")
        elif(dbdata==None):
            return render_template('login.html',mesg="Failed Login | User dosen't exists")

    if 'user' in session:
        return redirect(url_for('home'))

    return render_template('login.html',mesg="")





@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)

# with app.app_context():
#     db.create_all()