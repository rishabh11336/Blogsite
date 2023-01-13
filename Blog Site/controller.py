from flask import render_template, request, redirect, session, url_for
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
        userid = session['user_id']
        following = Following.query.filter_by(id=session['user_id'])
        post_list = []
        for i in following:
            list_of_post = Post.query.filter_by(id=i.following_id)
            _list = [i for i in list_of_post]
            post_list += _list
        n = len(post_list)
        for i in range(n):
            for j in range(0, n-i-1):
                if post_list[j].time > post_list[j+1].time:
                    post_list[j], post_list[j+1] = post_list[j+1], post_list[j]
        likes_list = []
        user_like = []
        for post in post_list:
            _like = Like.query.filter_by(post_id=post.post_id)
            likes_list = likes_list + [len([i for i in _like])]
            user_like = user_like + [ True if userid in [i.user_id for i in _like] else False ]
        post_tuple = [(post_list[i], likes_list[i], user_like[i]) for i in range(n)]
        return render_template("index.html", userid=userid, posts=post_tuple[::-1], likes=likes_list)
    else:
        return redirect('/sign-in')


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    if 'user_id' in session:
        userid = session['user_id']
        return render_template("index.html", userid=userid)
    return render_template('sign-in.html')


@app.route('/sign-up')
def sign_up():
    if 'user_id' in session:
        userid = session['user_id']
        return render_template("index.html", userid=userid)
    return render_template('sign-up.html')


@app.route('/<int:id>')
def profile(id):
    if 'user_id' in session:
        if session['user_id'] == id:
            userid = session['user_id']
            user = User.query.filter_by(id=session['user_id'])
            check = [i for i in user]
            print(check)
            following = Following.query.filter_by(id=session['user_id'])
            follower = len([i for i in following])
            followed = Following.query.filter_by(following_id=session['user_id'])
            follow = len([i for i in followed])
            qpost = Post.query.filter_by(id=userid)
            post_list = [i for i in qpost]
            post = len(post_list)
            return render_template('profile.html', post=post, user=check[0], latest_post=post_list[-1], follower=follower, follow=follow, id=id, userid=userid, follow_check='user')
        else:
            userid = session['user_id']
            user = User.query.filter_by(id=id)
            check = [i for i in user]
            print(check)
            following = Following.query.filter_by(id=id)
            follower = len([i for i in following])
            followed = Following.query.filter_by(following_id=id)
            follow = len([i for i in followed])
            qpost = Post.query.filter_by(id=id)
            post_list = [i for i in qpost]
            post = len(post_list)
            following_check = Following.query.filter_by(following_id=id, id=userid)
            follow_check = True if 1==len([i for i in following_check]) else False
            return render_template('profile.html', follow_check=follow_check, post=post, latest_post=post_list[-1], userid=userid, user=check[0], follower=follower, id=id, follow=follow, checkprofile='Follow')
    else:
        return redirect('/sign-in')


@app.route('/follow/<int:id>')
def follow(id):
    if 'user_id' in session:
        if session['user_id'] == id:
            userid = session['user_id']
            following = Following.query.filter_by(id=session['user_id'])
            follower = [i for i in following]
            followed = Following.query.filter_by(following_id=session['user_id'])
            follow = [i for i in followed]
            return render_template('follow.html',follow=follow,follower=follower, userid=userid)
        else:
            userid = session['user_id']
            following = Following.query.filter_by(id=id)
            follower = [i for i in following]
            followed = Following.query.filter_by(following_id=id)
            follow = [i for i in followed]
            return render_template('follow.html',follow=follow,follower=follower, userid=userid)
    else:
        return redirect('/sign-in')


@app.route('/search', methods=['GET','POST'])
def search():
    if 'user_id' in session:
        userid = session['user_id']
        search = request.form.get('search')
        print('search', search)
        users = User.query.all()
        user_list = []
        for user in users:
            if user.name == search or user.email == search:
                following_check = Following.query.filter_by(following_id=user.id, id=userid)
                follow_check = True if 1==len([i for i in following_check]) else False
                user_list += [(user,follow_check)] 
        return render_template('search.html', userid=userid, user_list=user_list)
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

@app.route('/post', methods=['POST'])
def post():
    if request.method == "POST":
        try:
            userobject = User.query.filter_by(id=session['user_id'])
            user = [i for i in userobject ]
            title = request.form.get("title")
            post = request.form.get("post")
            filename = None
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(session['user_id'], user[0].name, filename, post, title)
            updatepost = Post(id=session['user_id'], name=user[0].name, image=filename, post=post, title=title)
            db.session.add(updatepost)
            db.session.flush()
        except Exception as e:
            print('rollback')
            db.session.rollback()
            return "{}".format(e), "not posted"
        else:
            db.session.commit()
            return redirect('/')

@app.route('/blog/<int:id>')
def blog(id):
    if 'user_id' in session:
        if session['user_id'] == id:
            print(session['user_id'])
            userid = session['user_id']
            list_of_post = Post.query.filter_by(id=userid)
            post_list = [i for i in list_of_post[::-1]]
            delete = True
            n = len(post_list)
            likes_list = []
            user_like = []
            for post in post_list:
                _like = Like.query.filter_by(post_id=post.post_id)
                likes_list = likes_list + [len([i for i in _like])]
                user_like = user_like + [ True if userid in [i.user_id for i in _like] else False ]
            post_tuple = [(post_list[i], likes_list[i], user_like[i]) for i in range(n)]
            return render_template("blog.html", userid=userid, posts=post_tuple, delete=delete)
        else:
            print(session['user_id'])
            userid = session['user_id']
            list_of_post = Post.query.filter_by(id=id)
            post_list = [i for i in list_of_post[::-1]]
            delete = False
            n = len(post_list)
            likes_list = []
            user_like = []
            for post in post_list:
                _like = Like.query.filter_by(post_id=post.post_id)
                likes_list = likes_list + [len([i for i in _like])]
                user_like = user_like + [ True if userid in [i.user_id for i in _like] else False ]
            post_tuple = [(post_list[i], likes_list[i], user_like[i]) for i in range(n)]
            return render_template("blog.html", userid=userid, posts=post_tuple, delete=delete)
    else:
        return redirect('/sign-in')


@app.route('/follow-action/<int:id>')
def follow_action(id):
    if 'user_id' in session:
        try:
            user = User.query.filter_by(id=session['user_id'])
            check = [i for i in user]
            following_user = User.query.filter_by(id=id)
            check1 = [i for i in following_user]
            update_following = Following(id=session['user_id'], name=check[0].name, following_id=id, following=check1[0].name)
            db.session.add(update_following)
            db.session.flush()
        except Exception as e:
            print('rollback')
            db.session.rollback()
            return "{}".format(e), "not posted"
        else:
            db.session.commit()
            return redirect(url_for('profile', id=id))
    else:
        return redirect('/sign-in')

@app.route('/unfollow-action/<int:id>')
def unfollow_action(id):
    if 'user_id' in session:
        try:
            Following.query.filter_by(id=session['user_id'], following_id=id).delete()
            db.session.flush()
        except Exception as e:
            print('rollback')
            db.session.rollback()
            return "{}".format(e), "not posted"
        else:
            db.session.commit()
            return redirect(url_for('profile', id=id))
    else:
        return redirect('/sign-in')

@app.route('/profile-edit-action/<int:id>', methods=['GET','POST'])
def profile_action(id):
    if 'user_id' in session:
        if session['user_id'] != id:
            return redirect('/')
        if request.method == "GET":
            stud = User.query.filter_by(id=session['user_id'])
            check = [i for i in stud]
            return render_template("update_profile.html", user=check[0], userid=session['user_id'])

        elif request.method == "POST":
            try:
                cemail = request.form.get("email")
                cpassword = request.form.get("password")
                ccontact = request.form.get("contact_no")
                cname = request.form.get("name")
                cbio = request.form.get("bio")
                csex = request.form.getlist("sex")
                for i in csex[:1]:
                    user = User.query.filter_by(id=session['user_id'])
                    user_db = [i for i in user]
                    print(user_db[0].password,"db password", cpassword, "new password")
                    if user_db[0].password == cpassword:
                        user_db[0].email = cemail
                        user_db[0].password = cpassword
                        user_db[0].contact_no = ccontact
                        user_db[0].sex = i
                        user_db[0].name = cname
                        user_db[0].bio = cbio
                    else:
                        return "Wrong Password"
                db.session.flush()
            except Exception as e:
                print("rollback")
                db.session.rollback()
                return "{}".format(e),"not registered"
            else:
                db.session.commit()
                return redirect(url_for('profile', id=id))
    else:
        return redirect('/sign-in')

@app.route('/like-action/<int:post_id>')
def like_action(post_id):
    if 'user_id' in session:
        try:
            user = User.query.filter_by(id=session['user_id'])
            check = [i for i in user]
            update_like = Like(post_id=post_id, user_id=session['user_id'], name=check[0].name )
            db.session.add(update_like)
            db.session.flush()
        except Exception as e:
            print("rollback")
            db.session.rollback()
            return "{}".format(e),"not registered"
        else:
            db.session.commit()
            return redirect('/')
    else:
        return redirect('/sign-in')

@app.route('/unlike-action/<int:post_id>')
def unlike_action(post_id):
    if 'user_id' in session:
        try:
            Like.query.filter_by(post_id=post_id, user_id=session['user_id']).delete()
            db.session.flush()
        except Exception as e:
            print("rollback")
            db.session.rollback()
            return "{}".format(e),"not unliked"
        else:
            db.session.commit()
            return redirect('/')
    else:
        return redirect('/sign-in')

@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    if 'user_id' in session:
        try:
            Like.query.filter_by(post_id=post_id).delete()
            Post.query.filter_by(post_id=post_id, id=session['user_id']).delete()
            db.session.flush()
        except Exception as e:
            print("rollback")
            db.session.rollback()
            return "{}".format(e), "Not Deleted"
        else:
            db.session.commit()
            return redirect(url_for('blog', id=session['user_id']))
    else:
        return redirect('/sign-in')

@app.route('/edit-post/<int:post_id>', methods=['POST', 'GET'])
def edit_post(post_id):
    if 'user_id' in session:
        post = Post.query.filter_by(post_id=post_id)
        check = [i for i in post]
        if session['user_id'] != check[0].id:
            return redirect('/')
        if request.method == "GET":
            return render_template("edit_post.html", post=check[0], userid=session['user_id'])

        elif request.method == "POST":
            try:
                userobject = User.query.filter_by(id=session['user_id'])
                user = [i for i in userobject ]
                title = request.form.get("title")
                post = request.form.get("post")
                filename = None
                file = request.files['file']
                password = request.form.get("password")
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(session['user_id'], user[0].name, filename, post, title)
                updatepost = Post.query.filter_by(post_id=post_id)
                if password == user[0].password:
                    for i in updatepost:
                        if filename is not None:
                            i.image=filename
                        i.post=post
                        i.title=title
                else:
                    return "Wrong Password"
                db.session.flush()
            except Exception as e:
                print('rollback')
                db.session.rollback()
                return "{}".format(e), "not posted"
            else:
                db.session.commit()
                return redirect(url_for('blog', id=session['user_id']))
    else:
        return redirect('/sign-in')
