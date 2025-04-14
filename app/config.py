import os
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()

# Absolute path to the directory containing this config file
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')


    # Set absolute path to the uploads folder (relative to project root)
    UPLOAD_FOLDER = os.environ.get(
        'UPLOAD_FOLDER',
        os.path.abspath(os.path.join(basedir, '..', 'uploads'))
    )

    # Database connection
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:monopoly@localhost/lab5'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
