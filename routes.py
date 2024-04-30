from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from forms import RegistrationForm, LoginForm, MenuItemForm, OrderForm
from models import User, MenuItem, Order, CartItem

routes_app = Blueprint('routes', __name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляю, теперь вы зарегистрированы!')
        return redirect(url_for('login.html'))
    return render_template('register.html', title="Зарегистрироваться", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login.html'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('index.html'))
    return render_template('login.html', title="Войти", form=form)

@app.route("/logout", methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('index.html'))

@app.route("/menu", methods=['GET','POST'])
def menu():
    items = MenuItem.query.all()
    return render_template("menu.html", items=items)

@app.route("/add_item", methods=['GET','POST'])
def add_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        item = MenuItem(name=form.name.data, description=form.description.data, price=form.price.data)
        db.session.add(item)
        db.session.commit()
        flash('Успешно добавлено')
        return redirect(url_for('menu.html'))
    return render_template('add_item.html', title='Добавить в меню', form=form)

@app.route("/cart")
@login_required
def cart():
    cart_items = current_user.cart_items
    return render_template("cart.html", cart_items=cart_items)

@app.route("/add_to_cart/<int:item_id>", methods=['POST'])
@login_required
def add_to_cart(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if current_user.has_item_in_cart(item):
        flash('This item is already in your cart.', 'warning')
    else:
        cart_item = CartItem(user_id=current_user.id, menu_item_id=item.id)
        db.session.add(cart_item)
        db.session.commit()
        flash('Item added to your cart.', 'success')
    return redirect(url_for('menu.html'))

@app.route("/remove_from_cart/<int:item_id>", methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, menu_item_id=item_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from your cart.', 'success')
    return redirect(url_for('cart.html'))

@app.route("/order", methods=['GET','POST'])
@login_required
def order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(address=form.address.data, phone_number=form.phone_number.data, special_instruction=form.special_instructions.data, user_id=current_user.id)
        db.session.add(order)
        db.session.commit()
        flash("Спасибо за покупку!")
        return redirect(url_for('index.html'))
    return render_template('order.html', title='Заказать', form=form)