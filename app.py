from flask import Flask, redirect, render_template, url_for, request, session
# To generate the password hash
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector as sql

app = Flask(__name__)
app.secret_key = 'sgrtu444rufg'
conn = sql.connect(host='localhost', user='root', password='', database='register')
cur = conn.cursor()
@app.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        useremail = request.form['email']
        password1 = request.form['pass1']
        password2 = request.form['pass2']
        if password1 != password2:
            msg = "Password were not same!"
            return render_template ('register.html',msg=msg)
        cur.execute("SELECT * FROM login WHERE email=%s",(useremail,))
        us_email = cur.fetchone()
        if us_email:
            msg = "User Email Already Exist!"
            return render_template ('register.html', msg = msg)
        hash_password = generate_password_hash(password1)
        try:
            cur.execute("INSERT INTO login (name,email,password) VALUES (%s,%s,%s)",(username,useremail,hash_password))
            conn.commit()
            return render_template('login.html')
        except Exception as e:
            msg = (f'Error!', e)
            return render_template('register.html', msg= msg)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = conn.cursor(dictionary=True)
    if request.method == 'POST':
        useremail = request.form.get('email')
        userpassword = request.form.get('password')

        if not useremail or not userpassword:
            return render_template('login.html', msg="Email and password are required")

        cur.execute("SELECT * FROM login WHERE email=%s", (useremail,))
        user = cur.fetchone()

        if user and check_password_hash(user['password'], userpassword):
            session['useremail'] = user['name']
            return redirect(url_for('home'))
        else:
            msg = "Invalid Email or Password"
            return render_template('login.html', msg=msg)

    return render_template('login.html')


@app.route('/home')
def home():
    if 'useremail' in session:
        return render_template('home.html', username=session['useremail'])
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('useremail', None)

    return redirect(url_for('login'))    

if __name__ == "__main__":
    app.run(debug=True)