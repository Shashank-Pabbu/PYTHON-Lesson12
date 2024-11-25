from flask import Flask
from celery import Celery

# Initialize Flask app
app = Flask(__name__)

# Function to configure Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',  # Redis backend
        broker='redis://localhost:6379/0'    # Redis broker
    )
    celery.conf.update(app.config)
    return celery

# Initialize Celery instance
celery = make_celery(app)

# Define a sample Celery task
@celery.task
def long_running_task(x, y):
    return x + y
