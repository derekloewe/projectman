from datetime import datetime
import arrow
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), unique=True, nullable=False)
    supervisor_id = db.Column(db.Integer)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))
    name_first = db.Column(db.String(100), nullable=False)
    name_last = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)
    #account_name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow())
    #company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    about_me = db.Column(db.String(140))
    date_last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    image = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name_company = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user_group = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Company {self.name_company}>'


class Task_followers(UserMixin, db.Model):
    __tablename__ = 'task_followers'
    __table_args__ = (
        PrimaryKeyConstraint('task_id','follower_id'),
    )
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Task_follow {self.name_task}>'

    def follow(self, task):
        if not Task_followers.is_following(self, task):
            appe = Task_followers(follower_id=self.id, task_id=task)
            db.session.add(appe)
            db.session.commit()
            
    def unfollow(self, task):
        if Task_followers.is_following(self, task):
            task_r = Task_followers.query.filter(
                Task_followers.follower_id == self.id, Task_followers.task_id == task).first()
            db.session.delete(task_r)
            db.session.commit()

    def is_following(self, task):
          return Task_followers.query.filter(
            Task_followers.follower_id == self.id, Task_followers.task_id == task).count() > 0



class Task(UserMixin, db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(16000000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow())
    status = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Task {self.name_task}>'


    def my_tasks(self):
        #print(self.id)
        return Task.query.filter(Task.user_id == self.id)
        

#probably going to be errors
"""    def followed_task(self):
        return Task.query.join(
            task_followers, (task_followers.c.user_id == User.id)).filter(
                task_followers.c.task_id == self.id).order_by(
                    Task.date_created.desc()) """

    



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

