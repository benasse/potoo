from flask import Flask
from potoo.utils import get_config

config = get_config()

app = Flask(__name__,root_path='potoo')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = config['flask']['SECRET_KEY']

from potoo.routes import *
