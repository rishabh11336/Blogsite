from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
#session
app.secret_key=os.urandom(24)


#Model
from model import *
db.init_app(app)
app.app_context().push()
 
@app.route('/')
@app.route('/home')
def feeds():
    if 'user_id' in session:
        return render_template("index.html")
    else:
        return redirect('/sign-in')

@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    return render_template('sign-in.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/follow')
def follow():
    return render_template('follow.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/login-authentication', methods=['POST'])
def login():
    cemail = request.form.get("email")
    cpassword = request.form.get("password")
    print(cemail,"email")
    print(cpassword,"password")
    user = User.query.filter_by(email=cemail, password=cpassword)
    check = [i for i in user]
    print(check)
    if check:
        session['user_id'] = check[0].id
        print(session)
        print("authentication done")
        return redirect('/home')
    else:
        print("not found")
        return redirect('/')

@app.route('/logout')
def logout():
    print(session)
    session.pop('user_id')
    print('Logout')
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        try:
            cemail = request.form.get("email")
            cpassword = request.form.get("password")
            ccontact = request.form.get("contact_no")
            cname = request.form.get("name")
            csex = request.form.getlist("sex")
            for i in csex[:1]:
                update_user_db = User(email=cemail, password=cpassword, contact_no=ccontact, sex=i, name=cname)
            db.session.add(update_user_db)
            db.session.flush()
        except Exception as e:
            print(e,"e")
            print("rollback")
            db.session.rollback()
            return "{}".format(e),"not registered"
        else:
            db.session.commit()
            user = User.query.filter_by(email=cemail, password=cpassword)
            check = [i for i in user]
            print(check)
            if check:
                session['user_id'] = check[0].id
                print(session)
                print("authentication done")
                return redirect('/')
            else:
                print("not found")
                return redirect('/')
    return "not registered"

if __name__ == '__main__':
    app.run(debug=True)