from flask import Flask, request, render_template, redirect, flash
import mysql.connector as sql
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ksjfheit394jh' # Replace with a strong, randomly generated key

db = sql.connect(host='localhost', user='root', password='', database='register')
cur = db.cursor()



@app.route('/',methods=['GET','POST'])
def login():
    if request.method =='POST':
        Email = request.form['email']
        Password = request.form['password']
        cur.execute("SELECT * FROM login Where email=%s AND password =%s",(Email,Password))
        user_data = cur.fetchone()
        if user_data:
            return redirect ('home')
        else:
            return redirect('/')

        
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def Register():
    if request.method =='POST':
        Name = request.form.get('name')
        Email = request.form.get('email')
        Password = request.form.get('pass1')
        Confirm_password = request.form.get('pass2')
        if Password != Confirm_password:
            flash ("Password not same!. ")
            return redirect ('register')
        else:
            cur.execute("INSERT INTO login (name,email,pass1) VALUES(%s,%s,%s)",(Name,Email, Password))
            db.commit()
            flash ("SuccessFully Created!. ")
            return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    return "Welcome to Home Page! "

if __name__ == '__main__':
    app.run(debug=True)