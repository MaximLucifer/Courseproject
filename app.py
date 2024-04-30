from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

print(app.url_map)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    from models import User, MenuItem, Order
    from routes import index, register, login, logout, menu,  add_item, order
    from routes import routes_app
    app.register_blueprint(routes_app)
    app.run(debug=True)

