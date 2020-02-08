from datetime import datetime
import arrow
import time
from tzlocal import get_localzone
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import User, Task, Task_followers
from app.forms import LoginForm, RegistrationForm, EditProfileForm, TaskForm
from flask_login import current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb


from app.models import User, Task

Breadcrumbs(app=app)


@app.template_filter('local_time')
def local_time(time):   
    utc = arrow.get(datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S'))
    local_tz = get_localzone()
    #print(utc.to(local_tz))
    local=utc.to(local_tz).strftime("%m-%d-%Y %I %M:%S %p %Z")
    return local 

@app.template_filter('user_status')
def user_status(status):   
    if status == True:
        status_text = "Active"
    elif status == False:
        status_text = "Deactivated"
    return status_text 

        

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@register_breadcrumb(app, '.', 'Home')
def index():
    
    return render_template('index.html', title='Home', user=user, index=index)

@app.route('/login', methods=['GET', 'POST'])
@register_breadcrumb(app, '.login', 'Login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, login=login)

@app.route('/logout')
@register_breadcrumb(app, '.logout', 'Logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
@register_breadcrumb(app, '.register', 'Register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name_first=form.name_first.data, name_last=form.name_last.data, date_created=datetime.utcnow())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tasks = Task.my_tasks(current_user).all()
    return render_template('user.html', user=user, tasks=tasks)

@app.route('/user/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.image = form.image.data
        current_user.name_first = form.name_first.data
        current_user.name_last = form.name_last.data
        current_user.about_me = form.about_me.data
        current_user.date_modified = datetime.utcnow()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        user = current_user.username
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.name_first.data = current_user.name_first
        form.name_last.data = current_user.name_last
        form.image.data = current_user.image
        form.date_modified.data = current_user.date_modified
        #print(datetime.utcnow())
    return render_template('edit_profile.html', user=user, title='Edit Profile',
                           form=form)

@app.route('/tasks/create', methods=['GET', 'POST'])
@register_breadcrumb(app, '.tasks.create', 'Create')
@login_required
def task_create():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        t_i = Task_followers(task_id=task.id, follower_id=current_user.id)
        db.session.add(t_i)
        db.session.commit()
        flash('Task is now live')
        return redirect(url_for('tasks'))
    return render_template("tasks_create.html", title="Create Task", form=form, user=user)

#@app.route('/tasks')
@app.route('/tasks', methods=['GET', 'POST'])
@register_breadcrumb(app, '.tasks', 'Tasks')
@login_required
def tasks():
    user = current_user.id
    page = request.args.get('page', 1, type=int)
    tasks = Task.my_tasks(current_user).paginate(
        page, app.config['TASKS_PER_PAGE'], True)
    return render_template("tasks.html", title="Task's", tasks=tasks, user=user , page=page)

def view_task_dlc(*args, **kwargs):
    task_id = request.view_args['task_id']
    task = Task.query.get(task_id)
    return [{'text': task.name, 'url': task.id}]

@app.route('/tasks/<int:task_id>')
@register_breadcrumb(app, '.tasks.id', '',
                                 dynamic_list_constructor=view_task_dlc)
@login_required
def task(task_id):
    user = current_user
    task = Task.query.filter_by(id=task_id).first_or_404()
    return render_template('task.html', user=user, task=task)

@app.route('/dashboard')
@register_breadcrumb(app, '.dashboard', 'Dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user, dashboard=dashboard, title="Dashboard")

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.order_by(Task.date_created.desc()).paginate(
        page, app.config['TASKS_PER_PAGE'], False)
    return render_template("tasks.html", title="Explore", tasks=tasks.items)
    

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

