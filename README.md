# Niyo
Backend Developer Assessment

## Description 

The Task Management API is a powerful tool that allows users to efficiently manage their tasks. With this API, you can create tasks, edit tasks, delete tasks and view tasks. It provides a seamless and automated way to organize and prioritize tasks, helping individuals and teams stay on top of their workload.

## Usage

This API offers various endpoints for retriving data from the task management app.

### Endpoints Overview

> **:information_source: Notice:** Please replace `<baseUrl>` with the endpoint you are trying to access

| Endpoint      | Request Type  | Description       | Example Usage (bash)   |
| ------------- | ------------- | ----------------- | ---------------------- |
| `/users`  | POST  | For creating a new user   | `curl -X POST <baseUrl>/login -d '{"username": "username", "email address": "email@address.com", "password": "1234567932"} -H '"Content-Type" : "application/json"'`  |
| `/user/<string:user_id>`  | GET  | For getting user attributes   | `curl -X GET <baseUrl>/login  -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |
| `/user/<string:user_id>`  | PATCH  | For updating user attributes   | `curl -X PATCH <baseUrl>/login  -d '{"username": "Mary"}' -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |
| `/user/<string:user_id>`  | DELETE  | For deleting a user   | `curl -X DELETE <baseUrl>/login  -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |
| `/login`      | POST          | For Creating a token which can be used to login |  `curl -X POST <baseUrl>/login -d '{"email address": "email@address.com", "password": "1234567932"} -H '"Content-Type" : "application/json"'` |
| `/api/task/<string:task_id>`   | GET   | For Getting a single task    | `curl -X GET <baseUrl>/login -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |
| `/api/task/<string:task_id>`   | PATCH   | For updating a single task    | `curl -X PATCH <baseUrl>/login -d '"body": "Wash your cloths"' -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |
| `/api/task/<string:task_id>`   | DELETE   | For deleting a single task   | `curl -X DELETE <baseUrl>/login  -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |
| `/api/tasks`   | GET   | For Getting a all task    | `curl -X GET <baseUrl>/login -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |
| `/api/tasks`   | POST   | For creating task    | `curl -X PATCH <baseUrl>/login -d '{"title": "Task 1", "body": "Wash your cloths"}' -H '{"Content-Type" : "application/json", "Authorization": "<Token>}'`  |

## Installations

Follow the instructions here to run the API
```bash

# Getting the API Software
git clone https://


# To setup a virtual environment
virtualenv <name_of_virtualenv>

# Enter the virtual environment
<name_of_env>/scripts/activate

# Install the requirements
pip install -r requirements.txt

# Run the project
flask --app . run
```
