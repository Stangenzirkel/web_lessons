from flask import Flask, redirect, render_template
from flask_login import LoginManager, logout_user, login_required

from datetime import datetime
from flask import Flask, render_template, redirect, request
from data import db_session, jobs_api, user_api
from data.users import User
from data.jobs import Jobs, Type
from data.departments import Department
from forms.login import LoginForm
from forms.add_job import JobForm
from forms.register import RegisterForm
from forms.add_dep import DepForm
from flask_login import login_user, logout_user
from flask import make_response
from flask import jsonify
from requests import get

import os
print(os.getcwd())

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found - 404'}), 404)


@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed - 405'}), 405)


def main():
    db_session.global_init("db/project.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    app.run()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            param = dict()
            param["title"] = "Успех"
            param["list"] = user.speciality.split(", ")
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/user_show/<int:user_id>', methods=['GET', 'POST'])
def map(user_id):
    params = dict()
    params["title"] = "Карта пользователя"
    params["user"] = get(f'http://localhost:5000/api/user/{user_id}').json()['user']

    city = params["user"]["city_from"]
    map_mode = "map"
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": city,
        "format": "json"}

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": city,
        "format": "json"}

    response = get(geocoder_api_server, params=geocoder_params)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]

    static_api_server = "https://static-maps.yandex.ru/1.x/?"
    static_params = {
        "bbox": ','.join(toponym["lowerCorner"].split()) + '~' + ','.join(toponym["upperCorner"].split()),
        "l": map_mode
    }

    print(static_params["bbox"])

    response = get(static_api_server, params=static_params)
    with open('./static/img/img.png', "wb") as file:
        file.write(response.content)

    params["img"] = "map.png"
    print(params["user"])

    return render_template('map.html', **params)


@app.route('/', methods=['GET', 'POST'])
def works_log():
    params = dict()
    params["title"] = "Список задач"

    db_sess = db_session.create_session()
    params["works"] = list(map(lambda x: [x.job,
                                          [load_user(x.team_leader).surname + ' ' + load_user(x.team_leader).name, load_user(x.team_leader).id],
                                          x.work_size,
                                          x.collaborators,
                                          db_sess.query(Type).get(x.type).title,
                                          x.is_finished,
                                          str(x.id)],
                               db_sess.query(Jobs).all()))

    return render_template('works_log.html', **params)


@app.route('/departments', methods=['GET', 'POST'])
def deps_log():
    params = dict()
    params["title"] = "Список департаментов"

    db_sess = db_session.create_session()
    params["deps"] = list(map(lambda x: [x.title,
                                         [load_user(x.chief).surname + ' ' + load_user(x.chief).name, load_user(x.chief).id],
                                         x.members,
                                         x.email,
                                         str(x.id)],
                              db_sess.query(Department).all()))

    return render_template('deps_log.html', **params)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            type=form.type.data,
            is_finished=form.is_finished.data
        )
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Новая задача', form=form)


@app.route('/updjob/<int:id>', methods=['GET', 'POST'])
def update_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()

        form.team_leader.data = job.team_leader
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.type.data = job.type
        form.is_finished.data = job.is_finished

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.type = form.type.data
        job.is_finished = form.is_finished.data
        db_sess.commit()

        return redirect('/')
    return render_template('add_job.html', title='Изменение задачи', form=form)


@app.route('/deljob/<int:id>', methods=['GET', 'POST'])
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.route('/adddep', methods=['GET', 'POST'])
def add_dep():
    form = DepForm()
    if form.validate_on_submit():
        dep = Department(
            chief=form.chief.data,
            title=form.title.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess = db_session.create_session()
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_dep.html', title='Новый департамент', form=form)


@app.route('/upddep/<int:id>', methods=['GET', 'POST'])
def update_dep(id):
    form = DepForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()

        form.chief.data = dep.chief
        form.title.data = dep.title
        form.members.data = dep.members
        form.email.data = dep.email

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        dep.chief = form.chief.data
        dep.title = form.title.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.commit()

        return redirect('/departments')
    return render_template('add_dep.html', title='Изменение департамента', form=form)


@app.route('/deldep/<int:id>', methods=['GET', 'POST'])
def delete_dep(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).first()
    db_sess.delete(dep)
    db_sess.commit()
    return redirect('/departments')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()