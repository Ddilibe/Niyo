#!/usr/bin/env python3

from .utils import jwt_required, generate_token
from flask import request, jsonify
from flask.views import MethodView
from .models import User, Task
from uuid import uuid4
import json
import pdb


class UserParameterView(MethodView):

    def __init__(self, model):
        self.model = model

    @jwt_required
    def get(self, id):
        from .models import session
        new_user = session.query(User).filter(User.user_id==id).first()
        return jsonify(new_user.get_user_attributes()), 201

    @jwt_required
    def patch(self, id):
        from .models import session
        item = {key:value for key, value in json.loads(request.json).items() if key in ['username', 'email address']}
        new_user = session.query(User).filter(User.user_id==id).first()
        [setattr(new_user, key, value) for key, value in item.items()]
        session.commit()
        return jsonify(new_user.get_task_attributes().update({"info": "User attributes Updated"})), 201

    @jwt_required
    def delete(self, id):
        from .models import session
        new_user = session.query(User).filter(User.user_id==id).first()
        session.delete(new_user)
        session.commit()
        return jsonify({"info":"User Deleted"}), 201
    
class UserView(MethodView):

    def post(self):
        from .models import session
        data = json.loads(request.json)
        new_user = User(user_id=str(uuid4()), username=data['username'], email_address=data['email address'], password=data['password'])
        session.add(new_user)
        session.commit()
        return jsonify({'info': "New User Created"}), 201


class TaskParameterView(MethodView):

    def __init__(self, model):
        self.model = model

    @jwt_required
    def get(self, id):
        from .models import session
        new_task = session.query(Task).filter(Task.task_id==id).first()
        return jsonify(new_task.get_task_attributes()), 200
    
    @jwt_required
    def patch(self, id):
        from .models import session
        item = {key:value for key, value in json.loads(request.json).items() if key in ['title', 'body']}
        new_task = session.query(Task).filter(Task.task_id==id).first()
        [setattr(new_task, key, value) for key, value in item.items()]
        session.commit()
        new_task.get_task_attributes().update()
        return jsonify(new_task.get_task_attributes().update({"info": "Task Updated"})), 201

    @jwt_required
    def delete(self, id):
        from .models import session
        new_task = session.query(Task).filter(Task.task_id==id).first()
        session.delete(new_task)
        session.commit()
        return jsonify({"info":f"Task {id} deleted"}), 201
    

class TaskView(MethodView):

    @jwt_required
    def get(self):
        from .models import session
        all_task = {task.title : task.get_task_attribute() for task in session.query(Task).all() }
        return jsonify(all_task), 200

    @jwt_required
    def post(self, users):
        from .models import session
        data = request.json
        pdb.set_trace()
        new_task = Task(
            title=data['title'], body=data['body'], task_id=str(uuid4()),
            user=session.query(User).filter(User.user_id==self['user_id']).first().user_id
        )
        session.add(new_task)
        session.commit()
        return jsonify({'info': 'Task Created', "Task": {new_task.task_id}}), 201
    

def login():
    from .models import session
    data = request.json
    user = session.query(User).filter(User.email_address==data['email address']).first()
    password = user.verify_password(data['password'])
    if password:
        return jsonify({"token":generate_token(user.user_id), "info": "Login successful"}), 201
    else:
        return jsonify({"error": "Login Not Successful"}), 401
