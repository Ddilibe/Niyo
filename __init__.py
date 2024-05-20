#!/usr/bin/env python3

from .views import TaskView, UserView, login, TaskParameterView, UserParameterView
from .config import DevelopmentConfig
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__,)
app.config_class(DevelopmentConfig())
app.config['Debug'] = True
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/users", view_func=UserView.as_view('users'))
app.add_url_rule("/api/task", view_func=TaskView.as_view('tasks'))
app.add_url_rule("/user/<string:id>", view_func=UserParameterView.as_view('user'))
app.add_url_rule("/api/task/<string:id>", view_func=TaskParameterView.as_view('task'))

if "__main__" == __name__:
    app.debug = True
    app.run()