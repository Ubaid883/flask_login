from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)


@app.route('/')
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)