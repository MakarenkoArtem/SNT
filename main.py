from flask import Flask, render_template, redirect, request, session
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import sqlalchemy
from forms.event import EventForm
from data.event import Event
from forms.site import SiteForm
from data.users import User
from data.site import Site
from data import db_session
from os import listdir, remove, rmdir, mkdir, environ
from flask_login import LoginManager, current_user, login_user

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=1)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
users = {
    "admin": "password", "main_user": "pass"
}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@auth.verify_password
def verify_password(username, password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.name == username and check_password_hash(User.hashed_password, password)).all()
    if len(user):
        #user[0].date = datetime.datetime.now()
        login_user(user[0], remember=True)
        db_sess.commit()
        return user[0]
    '''
    if username in users and \
            check_password_hash(users.get(username), password):
        return username'''


@app.route('/del/<int:event>')
def del_event(event=-1):  # форма для регистрации
    db_sess = db_session.create_session()
    site = db_sess.query(Site).filter(User.id == 1).one()
    site.text = ", ".join([i for i in site.text.split(", ") if i != str(event)])
    db_sess.commit()
    return redirect('/')


@app.route('/<int:event>')
@app.route('/')
def main_list(event=-1):  # форма для регистрации
    print(listdir("static/img"))
    try:
        print("name:", current_user.name)
        admin = True
    except AttributeError:
        admin = False
    db_sess = db_session.create_session()
    try:
        site = db_sess.query(Site).filter(Site.id == 1).one()
    except sqlalchemy.exc.NoResultFound:
        return redirect('/change')
    except sqlalchemy.orm.exc.NoResultFound:
        return redirect('/change')
    s, text = [], []
    for i in site.text.split(", "):
        try:
            e = db_sess.query(Event).filter(Event.id == int(i)).one()
            s.append(i)
            text.append(e)
        except BaseException:
            pass
    site.text = ", ".join(s)
    db_sess.commit()
    return render_template('base.html', event_del=event, admin=admin,
                           text=text,  images=site.images.split(','),
                           docs_image=site.docs_image.split(','), oplata_image=site.oplata_image,
                           oplata_text=site.oplata_text, dolgi_image=site.dolgi_image)


@app.route('/change', methods=['GET', 'POST'])
@auth.login_required
def add():  # форма для добавления теста
    print("name:", auth.current_user().name)
    db_sess = db_session.create_session()
    form = SiteForm()
    if form.validate_on_submit():
        try:
            site = db_sess.query(Site).filter(Site.id == 1).one()
        except sqlalchemy.exc.NoResultFound:
            site = Site(id=1)
            db_sess.add(site)
        except sqlalchemy.orm.exc.NoResultFound:
            site = Site(id=1)
            db_sess.add(site)
        finally:
            [remove("static/img/" + i) for i in listdir("static/img") if
             i not in ['forest.jpg', "hello.gif", "nature.gif", "text.jpg"]]
            num_img = 1
            # site.text = form.text.data
            nums_img = []
            for i in form.images.data:
                image = i.read()
                if image == b'':
                    continue
                nums_img.append(str(num_img))
                with open(f'static/img/{num_img}.png', 'wb') as file:
                    file.write(image)
                num_img += 1
            site.images = ','.join(nums_img)
            nums_img = []
            for i in form.docs_image.data:
                image = i.read()
                if image == b'':
                    continue
                nums_img.append(str(num_img))
                with open(f'static/img/{num_img}.png', 'wb') as file:
                    file.write(image)
                num_img += 1
            site.docs_image = ','.join(nums_img)
            try:
                image = form.oplata_image.data.read()
                if image != b'':
                    site.oplata_image = str(num_img)
                    with open(f'static/img/{num_img}.png', 'wb') as file:
                        file.write(image)
                    num_img += 1
            except AttributeError:
                site.oplata_image = ""
            site.oplata_text = form.oplata_text.data
            try:
                image = form.dolgi_image.data.read()
                if image != b'':
                    site.dolgi_image = str(num_img)
                    with open(f'static/img/{num_img}.png', 'wb') as file:
                        file.write(image)
                    num_img += 1
            except AttributeError:
                site.dolgi_image = ""
            db_sess.commit()
        return redirect('/')
    return render_template('change.html', form=form)


@app.route('/event', methods=['GET', 'POST'])
@auth.login_required
def event():  # форма для добавления теста
    db_sess = db_session.create_session()
    form = EventForm()
    if form.validate_on_submit():
        try:
            site = db_sess.query(Site).filter(Site.id == 1).one()
        except sqlalchemy.exc.NoResultFound:
            site = Site(id=1)
            db_sess.add(site)
        except sqlalchemy.orm.exc.NoResultFound:
            site = Site(id=1)
            db_sess.add(site)
        finally:
            event = Event(text=form.text.data, znach=form.znach.data)
            db_sess.add(event)
            db_sess.commit()
            site.text = ", ".join(site.text.split(", ") + [str(event.id)])
            db_sess.commit()
        return redirect('/')
    return render_template('event.html', form=form)


def main():
    global users
    db_session.global_init()
    db_sess = db_session.create_session()
    try:
        mkdir("static/img")
    except FileExistsError:
        pass
    if 'HEROKU' in environ:
        users = {key.lstrip("USER_"): value for key, value in dict(environ).items() if
                 key[:5] == "USER_"}

    for key, value in users.items():
        try:
            db_sess.query(User).filter(User.name == key).one()
        except sqlalchemy.orm.exc.NoResultFound:
            user = User(name=key)
            user.set_password(value)
            db_sess.add(user)
            db_sess.commit()
    # users = {user.name: user.hashed_password for user in db_sess.query(User).all()}
    if 'HEROKU' in environ:
        port = int(environ.get("PORT", 5000))
        print(port)
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(port=8080, host='127.0.0.1', debug=False)


if __name__ == "__main__":
    main()
