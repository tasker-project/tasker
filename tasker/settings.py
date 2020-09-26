# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import os
import base64

from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
#SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", default='sqlite:///local.db')
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", default='postgresql://postgres:mb121691@localhost/tasker')
SECRET_KEY = env.str("SECRET_KEY", default=base64.b64encode(os.urandom(24)).decode('utf-8'))
SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT", default=5)
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
