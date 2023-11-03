from flask import Flask, request, render_template, redirect, session
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
from bson.json_util import dumps
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = 'ubion8'

with open("./mongoclient.txt", 'r', encoding='utf-8') as file:
    file_content = file.read()

client = MongoClient(file_content)
db = client.mylist

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_logged' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap
            
@app.route("/", methods=['GET', 'POST'])
def main():
    users = db.users
    ##username = request.form['username']
    #result = users.find_one({'username': username})

    name = '이승희'
    context = {"name" :name}
    return render_template('main.html', data = context)

@app.route("/auth", methods=['GET', 'POST'])
@is_logged_in
def auth():
    return "Success your Auth"
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        users = db.users
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = pbkdf2_sha256.hash(password)

        user = users.find_one({'email':email})
        if user:
            return redirect('/register')
        else:
          # print(username)
          users.insert_one({
              "username":username,
              "email":email,
              "password":password_hash
          })
          return redirect('/login')
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      users = db.users
      result = users.find_one({'email': email})

      if result:
        pw = result['password']
        auth = pbkdf2_sha256.verify(password, pw)
        print(auth)

        if auth == True:
            session['username'] = result['username']
            session['is_logged'] = True
            return redirect('/')
        else:
            return redirect('/login')
      else:
          return redirect('login')
        
    elif request.method == "GET":
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
if __name__ == '__main__':
    # print("TEST1")
    app.run(debug=True , port=8000)