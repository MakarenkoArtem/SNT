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
from config import users
from os import listdir, remove, rmdir, mkdir, environ
from flask_login import LoginManager, current_user, login_user
import fitz
from time import sleep

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=1)
app.config['SECRET_KEY'] = 'snt_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def load_images(form, end_str, site, del_imgs):
    num_img, nums_img, other_imgs = 1, [], []
    for i in form:
        if i.filename.endswith(".pdf"):
            img_pdf = []
            with open(f'static/{i.filename}', 'wb') as file:
                file.write(i.read())
            doc = fitz.open(f'static/{i.filename}')
            for n in range(len(doc)):
                page = doc.loadPage(n)  # number of page
                pix = page.getPixmap()
                output = f"static/img/{end_str}{num_img}.png"
                pix.writePNG(output)
                print(output)
                img_pdf.append(f"{end_str}{num_img}")
                num_img += 1
            doc.close()
            remove(f'static/{i.filename}')
            nums_img.append(";".join(img_pdf))
            continue
        image = i.read()
        if image == b'':
            continue
        other_imgs.append(f"{end_str}{num_img}")
        with open(f'static/img/{end_str}{num_img}.png', 'wb') as file:
            file.write(image)
        num_img += 1
    site = ','.join(nums_img + [";".join(other_imgs)])
    #nums_img = [f"{i}.png" for i in nums_img]
    del_imgs += list(set([i.rstrip(".png") for i in listdir("static/img") if i.startswith(end_str)]) - set(site.replace(";", ",").split(",")))
    return site, del_imgs


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    # print("id:", user_id)
    return db_sess.query(User).get(user_id)


@auth.verify_password
def verify_password(username, password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.name == username and check_password_hash(User.hashed_password, password)).all()
    if len(user):
        # user[0].date = datetime.datetime.now()
        # print("!", vars(current_user), user[0].name)
        if current_user is None or True:
            login_user(user[0], remember=True)
        db_sess.commit()
        return username
    '''
    if username in users and \
            check_password_hash(users.get(username), password):
        return username'''


@app.route('/edit/<int:event>', methods=['GET', 'POST'])
def edit_event(event):  # форма для регистрации
    try:
        print("name:", auth.current_user())
        if auth.current_user() is None:
            raise AttributeError
        admin = True
    except AttributeError:
        admin = False
    db_sess = db_session.create_session()
    form = EventForm()
    try:
        event = db_sess.query(Event).filter(Event.id == event).one()
        # except sqlalchemy.exc.NoResultFound:
        # site = Site(id=1)
        # db_sess.add(site)
        # site = db_sess.query(Site).filter(Site.id == 1).one()
    except sqlalchemy.orm.exc.NoResultFound:
        return redirect('/')
    print(1)
    if form.validate_on_submit():
        print(2)
        if "checkbox1" in list(dict(request.form).keys()):
            [remove(f"event_{i}.png") for i in event.images.split(", ")]
            num_img = max([int(i[6:].split(".")[0]) for i in listdir("static/img") if
                           i.startswith("event_")] + [1]) + 1
            nums_img = []
            for i in form.images.data:
                image = i.read()
                if image == b'':
                    continue
                nums_img.append(str(num_img))
                with open(f'static/img/event_{num_img}.png', 'wb') as file:
                    file.write(image)
                num_img += 1
            event.images = ", ".join(nums_img)
        event.text = form.text.data
        event.znach = form.znach.data
        db_sess.commit()
        return redirect('/')
    form.text.data = event.text
    form.znach.data = event.znach
    return render_template('event.html', form=form, edit=True)


@app.route('/del/<int:event>')
def del_event(event=-1):  # форма для регистрации
    db_sess = db_session.create_session()
    site = db_sess.query(Site).filter(User.id == 1).one()
    site.text = ", ".join([i for i in site.text.split(", ") if i != str(event)])
    db_sess.commit()
    return redirect('/#news')


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
    except sqlalchemy.orm.exc.NoResultFound:
        return redirect('/change')
    except sqlalchemy.exc.NoResultFound:
        return redirect('/change')
    s, text = [], []
    events = site.text.split(", ")
    events.sort()
    num_znach = 0
    for i in events:
        try:
            e = db_sess.query(Event).filter(Event.id == int(i)).one()
            if e.znach:
                s.insert(0, i)
                text.insert(0, e)
                num_znach += 1
            else:
                s.insert(num_znach, i)
                text.insert(num_znach, e)
        except BaseException:
            pass
    site.text = ", ".join(s)
    db_sess.commit()
    print([i.split(";") for i in site.images.split(',')])
    return render_template('base.html', event_del=event, admin=admin,
                           text=text, event_images=[i.images.split(", ")[:3] for i in text],
                           images=[i.split(";") for i in site.images.split(',')][0],
                           docs_image=[i.split(";") for i in site.docs_image.split(',')], oplata_image=[i.split(";") for i in site.oplata_image.split(',')],
                           oplata_text=site.oplata_text, dolgi_text=site.dolgi_text)


@app.route('/change', methods=['GET', 'POST'])
@auth.login_required
def add():  # форма для добавления теста
    try:
        print("name:", auth.current_user())
        if auth.current_user() is None:
            raise AttributeError
        admin = True
    except AttributeError:
        admin = False
    db_sess = db_session.create_session()
    form = SiteForm()
    try:
        site = db_sess.query(Site).filter(Site.id == 1).one()
        # except sqlalchemy.exc.NoResultFound:
        # site = Site(id=1)
        # db_sess.add(site)
        # site = db_sess.query(Site).filter(Site.id == 1).one()
    except sqlalchemy.orm.exc.NoResultFound:
        site = Site(id=1, text="")
        db_sess.add(site)
        db_sess.commit()
        site = db_sess.query(Site).filter(Site.id == 1).one()
    if form.validate_on_submit():
        del_imgs = []
        if "checkbox1" in list(dict(request.form).keys()):
            site.images, del_imgs = load_images(form.images.data, "im_", site.images, del_imgs)
        if "checkbox2" in list(dict(request.form).keys()):
            site.docs_image, del_imgs = load_images(form.docs_image.data, "docs_", site.docs_image, del_imgs)
        if "checkbox3" in list(dict(request.form).keys()):
            site.oplata_image, del_imgs = load_images(form.oplata_image.data, "oplata_", site.oplata_image, del_imgs)
        #if "checkbox4" in list(dict(request.form).keys()):
        site.oplata_text = form.oplata_text.data
        #if "checkbox5" in list(dict(request.form).keys()):
        site.dolgi_text = form.dolgi_text.data
        # site.dolgi_image, del_imgs = load_images(form.dolgi_image.data, "dolgi_", site.dolgi_image, del_imgs)
        db_sess.add(site)
        db_sess.commit()
        [remove(f"static/img/{i}") for i in del_imgs]
        return redirect('/')
    form.oplata_text.data = site.oplata_text
    form.dolgi_text.data = site.dolgi_text
    return render_template('change.html', form=form)


@app.route('/event', methods=['GET', 'POST'])
@auth.login_required
def event():  # форма для добавления теста
    try:
        print("name:", auth.current_user())
        if auth.current_user() is None:
            raise AttributeError
        admin = True
    except AttributeError:
        admin = False
    db_sess = db_session.create_session()
    form = EventForm()
    if form.validate_on_submit():
        try:
            site = db_sess.query(Site).filter(Site.id == 1).one()
            # except sqlalchemy.exc.NoResultFound:
            # site = Site(id=1)
            # db_sess.add(site)
        except sqlalchemy.orm.exc.NoResultFound:
            site = Site(id=1, text="")
            db_sess.add(site)
            db_sess.commit()
            site = db_sess.query(Site).filter(Site.id == 1).one()
        finally:
            num_img = max([int(i[6:].split(".")[0]) for i in listdir("static/img") if
                           i.startswith("event_")] + [1]) + 1
            nums_img = []
            for i in form.images.data:
                image = i.read()
                if image == b'':
                    continue
                nums_img.append(str(num_img))
                with open(f'static/img/event_{num_img}.png', 'wb') as file:
                    file.write(image)
                num_img += 1
            event = Event(text=form.text.data, images=", ".join(nums_img), znach=form.znach.data)
            db_sess.add(event)
            db_sess.commit()
            site.text = ", ".join(site.text.split(", ") + [str(event.id)])
            db_sess.commit()
        return redirect('/')
    return render_template('event.html', form=form, edit=False)


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
        app.run(host='0.0.0.0', port=port)
    else:
        # app.run(port=8080, host='127.0.0.1', debug=False)
        app.run(port=5000, host='89.223.100.101', debug=False)


if __name__ == "__main__":
    main()
