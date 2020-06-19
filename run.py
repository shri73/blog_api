import os
from app import create_app

if __name__ == '__main__':
    # Get flask env 'development' from env
    env_name = os.getenv("FLASK_ENV")
    app = create_app(env_name)
    app.run()
