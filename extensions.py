#----------------------------------------------------------------------------#
# App extensions and config
#----------------------------------------------------------------------------#

from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')

moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
