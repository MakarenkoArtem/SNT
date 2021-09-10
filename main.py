from flask import Flask, render_template, redirect, request, session
import datetime
from os import listdir, remove, rmdir, mkdir, environ
app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=1)
app.config['SECRET_KEY'] = 'secret_key'
@app.route('/')
def main_list():  # форма для регистрации
    return render_template('base.html')


def main():
    try:
        mkdir("static/img")
    except FileExistsError:
        pass
    if 'HEROKU' in environ:
        port = int(environ.get("PORT", 5000))
        print(port)
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(port=8080, host='127.0.0.1', debug=False)


if __name__ == "__main__":
    main()
