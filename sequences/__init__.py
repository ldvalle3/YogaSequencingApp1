from logging.handlers import RotatingFileHandler
from flask import Flask, logging
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sequencing.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# Initialize OAuth for Auth0
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='dRvSOehspvYOw7M21xDtPHpaijFWb1s5',
    client_secret='lJ-lzvbpGzRpKJstAGvNZcwNqlRDeg5NsJIim1JvlBo27FNGH84JNC3z7su-j7PT',
    api_base_url='https://dev-b1chlna5prtx13oi.us.auth0.com',
    access_token_url='https://dev-b1chlna5prtx13oi.us.auth0.com/oauth/token',
    authorize_url='https://dev-b1chlna5prtx13oi.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
    discovery_endpoint='https://dev-b1chlna5prtx13oi.us.auth0.com/.well-known/openid-configuration'
)

# Logging configuration
if not app.debug:  # Only log in production mode
    # Log to a file with rotating logs
    file_handler = RotatingFileHandler('logs/security.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    # Set log level for the app
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application Startup')

from sequences import routes
