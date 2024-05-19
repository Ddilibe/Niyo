#!/usr/bin/env python3

import os

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")

class DevelopmentConfig(Config):

    debug = True
    
