from flask import Flask
from models import db, bcrypt
from config import app_config
from views.UserView import user_api as user_blueprint
from views.BlogpostView import blog_post_api as blogpost_blueprint


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    # initializing bcrypt
    bcrypt.init_app(app)  

    db.init_app(app)
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
    app.register_blueprint(blogpost_blueprint, url_prefix='/api/v1/blogposts')

    return app
