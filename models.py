#!/usr/bin/env python3

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

Base = declarative_base()

class User(Base):

    __tablename__ = "User"
    user_id = Column(String(225), primary_key=True)
    username = Column(String(18), nullable=False)
    email_address = Column(String(255), nullable = False)
    password_hash = Column(String(255), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    task = Column(String(128), ForeignKey('Task.task_id'))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = str(generate_password_hash(password))

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_user_attributes(self):
        return{
            "Username":self.username, "Email Address": self.email_address,
            "Created On": self.created_on, "Updated On": self.updated_on, 'user_id':self.user_id
        }
    

class Task(Base):

    __tablename__ = "Task"
    task_id = Column(String(225), primary_key=True)
    title = Column(String(128), nullable=False)
    body = Text()
    created_on = Column(DateTime(), default=datetime.now)
    user = relationship("User", backref=backref('Task', order_by=created_on))

    def get_task_attributes(self):
        return {
            "Title": self.title, "Body": self.body,'task_id': self.task_id,
            'Created On': self.created_on, "User": self.user.username
        }


engine = create_engine(f'sqlite:///{os.curdir}/task.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session =  Session()
