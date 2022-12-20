from flask_migrate import Migrate
from app.ext import db
from app import create_app
from config import Config

if __name__ == '__main__':
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=Config.DEBUG)
