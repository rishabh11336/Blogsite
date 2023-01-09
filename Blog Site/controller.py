from flask import render_template, request, redirect, session
from main import app
from werkzeug.utils import secure_filename
from model import *
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/')
@app.route('/home')
def feeds():
    if 'user_id' in session:
        print(session['user_id'])
        return render_template("index.html")
    else:
        return redirect('/sign-in')


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    if 'user_id' in session:
        return render_template("index.html")
    return render_template('sign-in.html')


@app.route('/sign-up')
def sign_up():
    if 'user_id' in session:
        return render_template("index.html")
    return render_template('sign-up.html')


@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id'])
        check = [i for i in user]
        print(check)
        following = Following.query.filter_by(id=session['user_id'])
        follower = len([i for i in following])
        return render_template('profile.html', user=check[0], follower=follower, follow=00)
    else:
        return redirect('/sign-in')


@app.route('/follow')
def follow():
    if 'user_id' in session:
        return render_template('follow.html')
    else:
        return redirect('/sign-in')


@app.route('/search')
def search():
    if 'user_id' in session:
        return render_template('search.html')
    else:
        return redirect('/sign-in')


@app.route('/login-authentication', methods=['POST'])
def login():
    cemail = request.form.get("email")
    cpassword = request.form.get("password")
    user = User.query.filter_by(email=cemail, password=cpassword)
    check = [i for i in user]
    if check:
        session['user_id'] = check[0].id
        print(session['user_id'])
        print("authentication done")
        return redirect('/home')
    else:
        print("not found")
        return redirect('/')


@app.route('/logout')
def logout():
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
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            csex = request.form.getlist("sex")
            for i in csex[:1]:
                update_user_db = User(email=cemail, password=cpassword, contact_no=ccontact, sex=i, name=cname, profile_pic=filename, bio="write about yourself")
            db.session.add(update_user_db)
            db.session.flush()
        except Exception as e:
            print("rollback")
            db.session.rollback()
            return "{}".format(e),"not registered"
        else:
            db.session.commit()
            user = User.query.filter_by(email=cemail, password=cpassword)
            check = [i for i in user]
            if check:
                session['user_id'] = check[0].id
                return redirect('/')