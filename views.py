#!/usr/bin/env python3

from .utils import jwt_required, generate_token
from flask import request, jsonify
from flask.views import MethodView
from .models import User, Task
from uuid import uuid4
import json
import pdb


class UserParameterView(MethodView):
    """
    Represents the API endpoint for performing operations on a specific User.

    Methods:
    get(self, id: str) -> JSONResponse:
        Retrieves details of a user identified by the given ID.
    
    patch(self, id: str) -> JSONResponse:
        Updates specific attributes of a user identified by the given ID.
    
    delete(self, id: str) -> JSONResponse:
        Deletes a user identified by the given ID.
    """

    @jwt_required
    def get(self, id):
        """
        GET method to retrieve details of a user.

        Arguments:
        @id:str - The unique identifier of the user to retrieve.

        Returns:
        JSONResponse: A JSON response containing user attributes if successful, else error response.
        """
        from .models import session
        new_user = session.query(User).filter(User.user_id==id).first()
        return jsonify(new_user.get_user_attributes()), 201

    @jwt_required
    def patch(self, id):
        """
        PATCH method to update specific attributes of a user.

        Arguments:
        @id:str - The unique identifier of the user to update.

        Returns:
        JSONResponse: A JSON response confirming the update if successful, else error response.
        """
        from .models import session
        item = {key:value for key, value in json.loads(request.json).items() if key in ['username', 'email address']}
        new_user = session.query(User).filter(User.user_id==id).first()
        [setattr(new_user, key, value) for key, value in item.items()]
        session.commit()
        return jsonify(new_user.get_task_attributes().update({"info": "User attributes Updated"})), 201

    @jwt_required
    def delete(self, id):
        """
        DELETE method to delete a user.

        Arguments:
        @id:str - The unique identifier of the user to delete.

        Returns:
        JSONResponse: A JSON response confirming the deletion if successful, else error response.
        """
        from .models import session
        new_user = session.query(User).filter(User.user_id==id).first()
        session.delete(new_user)
        session.commit()
        return jsonify({"info":"User Deleted"}), 201
    
class UserView(MethodView):
    """
    Represents the API endpoint for creating a new User.

    Methods:
    post(self) -> JSONResponse:
        Creates a new user based on the provided data.
    """

    def post(self):
        """
        POST method to create a new user.

        Returns:
        JSONResponse: A JSON response confirming the creation of a new user if successful, else error response.
        """
        from .models import session
        data = json.loads(request.json)
        new_user = User(user_id=str(uuid4()), username=data['username'], email_address=data['email address'], password=data['password'])
        session.add(new_user)
        session.commit()
        return jsonify({'info': "New User Created"}), 201


class TaskParameterView(MethodView):
    """
    Represents the API endpoint for performing operations on a specific Task.

    Methods:
    get(self, id: str) -> JSONResponse:
        Retrieves details of a task identified by the given ID.
    
    patch(self, id: str) -> JSONResponse:
        Updates specific attributes of a task identified by the given ID.
    
    delete(self, id: str) -> JSONResponse:
        Deletes a task identified by the given ID.
    """

    @jwt_required
    def get(self, id):
        """
        GET method to retrieve details of a task.

        Arguments:
        @id:str - The unique identifier of the task to retrieve.

        Returns:
        JSONResponse: A JSON response containing task attributes if successful, else error response.
        """
        from .models import session
        new_task = session.query(Task).filter(Task.task_id==id).first()
        return jsonify(new_task.get_task_attributes()), 200
    
    @jwt_required
    def patch(self, id):
        """
        PATCH method to update specific attributes of a task.

        Arguments:
        @id:str - The unique identifier of the task to update.

        Returns:
        JSONResponse: A JSON response confirming the update if successful, else error response.
        """
        from .models import session
        item = {key:value for key, value in json.loads(request.json).items() if key in ['title', 'body']}
        new_task = session.query(Task).filter(Task.task_id==id).first()
        [setattr(new_task, key, value) for key, value in item.items()]
        session.commit()
        new_task.get_task_attributes().update()
        return jsonify(new_task.get_task_attributes().update({"info": "Task Updated"})), 201

    @jwt_required
    def delete(self, id):
        """
        DELETE method to delete a task.

        Arguments:
        @id:str - The unique identifier of the task to delete.

        Returns:
        JSONResponse: A JSON response confirming the deletion if successful, else error response.
        """
        from .models import session
        new_task = session.query(Task).filter(Task.task_id==id).first()
        session.delete(new_task)
        session.commit()
        return jsonify({"info":f"Task {id} deleted"}), 201
    

class TaskView(MethodView):
    """
    Represents the API endpoint for handling tasks.

    Methods:
    get(self) -> JSONResponse:
        Retrieves details of all tasks.
    
    post(self, users: Dict) -> JSONResponse:
        Creates a new task based on the provided data.
    """

    @jwt_required
    def get(self):
        """
        GET method to retrieve details of all tasks.

        Returns:
        JSONResponse: A JSON response containing details of all tasks if successful, else error response.
        """
        from .models import session
        all_task = {task.title : task.get_task_attribute() for task in session.query(Task).all() }
        return jsonify(all_task), 200

    @jwt_required
    def post(self, users):
        """
        POST method to create a new task.

        Arguments:
        @users:Dict - List of users to associate with the task.

        Returns:
        JSONResponse: A JSON response confirming the creation of a new task if successful, else error response.
        """
        from .models import session
        data = request.json
        new_task = Task(
            title=data['title'], body=data['body'], task_id=str(uuid4()),
            user=session.query(User).filter(User.user_id==self['user_id']).first().user_id
        )
        session.add(new_task)
        session.commit()
        return jsonify({'info': 'Task Created', "Task": {new_task.task_id}}), 201
    

def login():
    """
    Handles user login authentication.

    Returns:
    JSONResponse: A JSON response containing a JWT token and login information if successful, else error response.
    """
    from .models import session
    data = request.json
    user = session.query(User).filter(User.email_address==data['email address']).first()
    password = user.verify_password(data['password'])
    if password:
        return jsonify({"token":generate_token(user.user_id), "info": "Login successful"}), 201
    else:
        return jsonify({"error": "Login Not Successful"}), 401
