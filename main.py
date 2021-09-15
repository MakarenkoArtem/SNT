from flask import Flask, render_template, redirect, request, session
import datetime
import sqlalchemy
from forms.site import SiteForm
from data.site import Site
from data import db_session
from os import listdir, remove, rmdir, mkdir, environ

app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=1)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
def main_list():  # форма для регистрации
    db_sess = db_session.create_session()
    site = db_sess.query(Site).filter(Site.id == 1).one()
    return render_template('base.html', text=site.text.split("\n"), images=site.images.split(','),
                           docs_image=site.docs_image.split(','), oplata_image=site.oplata_image,
                           oplata_text=site.oplata_text, dolgi_image=site.dolgi_image)


@app.route('/change', methods=['GET', 'POST'])
def add():  # форма для добавления теста
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
        except BaseException as e:
            print(e.__name__)
            site = Site(id=1)
            db_sess.add(site)
        finally:
            [remove("static/img/" + i) for i in listdir("static/img") if i not in ['forest.jpg', "hello.gif", "nature.gif", "text.jpg"]]
            num_img = 1
            site.text = form.text.data
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


def main():
    db_session.global_init()
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
