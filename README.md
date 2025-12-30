![GitHub](https://img.shields.io/github/license/rishabh11336/Blogsite)
![GitHub repo size](https://img.shields.io/github/repo-size/rishabh11336/Blogsite)
# Bloglite
## create virtual enviroment
```
command: pip install virtualenv
```
```
command: virtualenv <venv_name>
```
## Learn more about virtual enviroment refer to
```
https://medium.com/@asusrishabh/requirements-txt-in-python-947b0b43bbe6
```
- use requirements.txt to install compatible packages
```
command: pip install -r requirements.txt
```
- To run flask server
```
command: python main.py
```

## Supabase Database Setup (PostgreSQL)

### Option 1: Using Supabase PostgreSQL (Recommended)

1. **Configure Environment Variables**
   ```bash
   cd Blog_Site
   # Edit .env file and replace [YOUR-PASSWORD] with your database password
   nano .env  # or use any text editor
   ```

2. **Initialize Database**
   ```bash
   conda run -n blogsite python init_supabase_db.py
   ```

3. **(Optional) Migrate Existing SQLite Data**
   ```bash
   # Backup SQLite first
   cp database.sqlite3 database.sqlite3.backup
   
   # Run migration
   conda run -n blogsite python migrate_sqlite_to_supabase.py
   ```

4. **Start Application**
   ```bash
   conda run -n blogsite python main.py
   ```
   Access at: http://localhost:8080

### Option 2: Using SQLite (Development Only)

Simply remove or rename the .env file, and the application will use SQLite automatically:
```bash
cd Blog_Site
mv .env .env.backup
python main.py
```


## Description
Bloglite is a simple blog application like Instagram, twitter or Linkedin, It is a multi user app with
login, feed, post/blog, with various features like follow/unfollow, edit profile/post and search.<br>
This consist of two APIs for CRUD operation on USER and BLOG/POST
- Technologies used
1. Python (Programming Language)
2. Flask (Web Framework)
3. HTML (HTML Doc.)
4. Bootstrap (Frontend)
5. Flask-RESTful==0.3.9 (RESTAPIs)
6. Flask-SQLAlchemy==3.0.2 (SQLite connection)
7. Jinja2==3.1.2 (HTML injection)
8. SQLAlchemy==1.4.45 (SQLite connection)
9. Werkzeug==2.2.2 ( To secure file)

## APIs are for CRUD Operation on USER & BLOG/POST
- For UserAPI
```
GET:- localhost:8080/users/{userid}
```
```
POST:- localhost:8080/users/
```
```
PUT:- localhost:8080/users/{userid}
```
```
DELETE:- localhost:8080/users/{userid}
```
- For POST/BLOG_API
```
GET:- localhost:8080/posts/{postid}
```
```
POST:- localhost:8080/posts/
```
```
PUT:- localhost:8080/posts/{postid}
```
```
DELETE:- localhost:8080/posts/{postid}
```
#### (check API.pdf for hints to check APIs)
## DB Schema Design
![image](https://user-images.githubusercontent.com/67859818/218969616-cdd254ba-9204-4f4f-9482-bbf4a13043e9.png)

# 
└── Blog Site<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── static<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── templates<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── api.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── main.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── controller.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── model.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── requirements.txt<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── database.sqlite3<br>

### [Wireframe: Blog.png](https://github.com/rishabh11336/Blogsite/blob/main/Blog.png)
### [Looking for email and password for webapp](https://github.com/rishabh11336/Blogsite/blob/main/Blog%20Site/README.md#for-testing-username-in-current-database)
