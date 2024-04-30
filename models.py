from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    order = db.relationship('Order', backref='customer', lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Float) 

    def __repr__(self):
        return '<MenuItem {}>'.format(self.name)
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    menu_item = db.relationship('MenuItem', backref='cart_items')

    def __repr__(self):
        return f"CartItem(id={self.id}, user_id={self.user_id}, menu_item_id={self.menu_item_id}, quantity={self.quantity})"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    special_instructions = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Order {}>".format(self.id)