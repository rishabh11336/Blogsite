from flask import Flask, render_template
 
app = Flask(__name__)
 
@app.route('/')
def feeds():
    return render_template("index.html")

@app.route('/sign')
def sign_in():
    return render_template('sign.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/follow')
def follow():
    return render_template('follow.html')

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)