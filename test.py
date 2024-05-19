#!/usr/bin/env python3

import requests
import json

url = "http://127.0.0.1:5000"
data = {
    "username": "Mangino", "email address": "man@gin.com", "password": "1234567932",
}
head = {
    "Content-Type" : 'application/json'
}

# Create User
user = requests.post(f'{url}/users', json=json.dumps(data), headers=head)
print("For Signup", user.text)

# Login

data.update(user.json())
# user = requests.post(f"{url}/login", data=json.dumps(data))
# print("For Login", user.json())