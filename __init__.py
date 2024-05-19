#!/usr/bin/env python3

from .views import TaskView, UserView, login, TaskParameterView, UserParameterView
from sqlalchemy.orm import sessionmaker
from .config import DevelopmentConfig
from sqlalchemy import create_engine
from .models import create_database
from flask import Flask

engine = create_engine('sqlite:///:memory:')
app = Flask(__name__,)
app.config_class(DevelopmentConfig())
app.config['Debug'] = True
Session = sessionmaker(bind=engine)
session = Session()
create_database()
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/users", view_func=UserView.as_view('users'))
app.add_url_rule("/api/task", view_func=TaskView.as_view('tasks'))
app.add_url_rule("/user/<string:id>", view_func=UserParameterView.as_view('user'))
app.add_url_rule("/api/task/<string:id>", view_func=TaskParameterView.as_view('task'))