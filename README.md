# Blogsite

<h1>for virtual enviroment</h1>
<strong>command: <i>pip install virtualenv</i></strong> <br><br>
<strong>command: <i>virtualenv venv_name</i> </strong> <br>
<h2>to learn more about venv refer to</h2>
https://medium.com/@asusrishabh/requirements-txt-in-python-947b0b43bbe6

<br>
<h2>use requirement.txt to install compatible packages</h2>
<strong>command: <i>pip install -r requirment.txt</i></strong><br>
<h2> To run flask server</h2>
<strong>command: <i>python main.py</i></strong>

### Wireframe: Blog.png

## Description
Bolglite is a simple blog application like Instagram, twitter or Linkedin, It is a multi user app with
login, feed, post/blog, with various features like follow/unfollow, edit profile/post and search.<br>
This consist of two APIs for CRUD operation on USER and BLOG/POST
Technologies used
1. Python (Programming Language)
2. Flask (Web Framework)
3. HTML (HTML Doc.)
4. Bootstrap (Frontend)
5. Flask-RESTful==0.3.9 (RESTAPIs)
6. Flask-SQLAlchemy==3.0.2 (SQLite connection)
7. Jinja2==3.1.2 (HTML injection)
8. SQLAlchemy==1.4.45 (SQLite connection)
9. Werkzeug==2.2.2 ( To secure file)
# API Design
### APIs are for CRUD Operation on USER & BLOG/POST
### For UserAPI
GET:- localhost:8080/users/{userid}<br>
POST:- localhost:8080/users/<br>
PUT:- localhost:8080/users/{userid}<br>
DELETE:- localhost:8080/users/{userid}<br>
### For POST/BLOG_API
GET:- localhost:8080/posts/{postid}<br>
POST:- localhost:8080/posts/<br>
PUT:- localhost:8080/posts/{postid}<br>
DELETE:- localhost:8080/posts/{postid}<br>
#### (check API.pdf for hints to check APIs)
## DB Schema Design
![image](https://user-images.githubusercontent.com/67859818/218969616-cdd254ba-9204-4f4f-9482-bbf4a13043e9.png)

#### Architecture and Features
└── Blog Site<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── static<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── templates<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── api.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── main.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── controller.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── model.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── requirement.txt<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── database.sqlite3<br>

