import flask
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json
import math
import pymysql

pymysql.install_as_MySQLdb()  # Use PyMySQL as MySQLdb substitute

# Load configuration from config.json
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = params['local_server']

app = Flask(__name__)
app.secret_key = "secret-key"
app.config['IMAGE_UPLOAD_FOLDER'] = params['image_upload_location']

# Mail server configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pass']
)
mail = Mail(app)

# Database configuration
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


# Database models
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)  # Changed to String
    message = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime, nullable=True)  # Changed to DateTime


class ShopItems(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Changed to Float
    saleprice = db.Column(db.Float, nullable=False)  # Changed to Float
    info = db.Column(db.String(2000), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=True)  # Changed to DateTime
    imgfile = db.Column(db.String(255), nullable=True)


@app.route("/")
def home():
    return render_template('cover/index.html', params=params)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin-user']:
        items = ShopItems.query.all()
        return render_template('shop/dashboard.html', params=params, items=items)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('upass')
        if username == params['admin-user'] and userpass == params['admin-pass']:
            session['user'] = username
            items = ShopItems.query.all()
            return render_template('shop/dashboard.html', params=params, items=items)
        else:
            return redirect('/dashboard')
    else:
        return render_template('shop/login.html', params=params)


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit_item(sno):
    if 'user' in session and session['user'] == params['admin-user']:
        item = ShopItems.query.filter_by(sno=sno).first()
        if request.method == 'POST':
            new_slug = request.form.get('slug')
            new_name = request.form.get('name')
            new_price = float(request.form.get('price'))
            new_sale_price = float(request.form.get('sale_price'))
            new_info = request.form.get('info')
            new_manufacturer = request.form.get('manufacturer')

            # File upload handling
            if 'image' in request.files:
                f = request.files['image']
                if f.filename != '':
                    f.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], secure_filename(f.filename)))
                    new_image = f.filename
                else:
                    new_image = item.imgfile if item else ''

            if sno == '0':
                entry = ShopItems(slug=new_slug, name=new_name, price=new_price,
                                  saleprice=new_sale_price, info=new_info,
                                  manufacturer=new_manufacturer, date=datetime.now(),
                                  imgfile=new_image)
                db.session.add(entry)
                db.session.commit()
            else:
                item.slug = new_slug
                item.name = new_name
                item.price = new_price
                item.saleprice = new_sale_price
                item.info = new_info
                item.manufacturer = new_manufacturer
                item.imgfile = new_image
                item.date = datetime.now()
                db.session.commit()
                return redirect('/edit/' + sno)
        return render_template('shop/edit.html', params=params, item=item, sno=sno)


@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete_item(sno):
    if 'user' in session and session['user'] == params['admin-user']:
        item = ShopItems.query.filter_by(sno=sno).first()
        db.session.delete(item)
        db.session.commit()
    return redirect('/dashboard')


@app.route("/shop")
def shop():
    page = request.args.get('page', 1, type=int)
    items = ShopItems.query.paginate(page=page, per_page=int(params['no_of_items_on_shop']))
    return render_template('shop/index.html', params=params, items=items)


@app.route("/item/<string:item_slug>", methods=['GET'])
def item_route(item_slug):
    item = ShopItems.query.filter_by(slug=item_slug).first()
    items = ShopItems.query.limit(int(params['related_items'])).all()
    return render_template('shop/shop-item.html', params=params, item=item, items=items)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_no=phone, message=message, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        try:
            mail.send_message('New query from project by ' + name,
                              sender=params['gmail-user'],
                              recipients=[params['gmail-user']],
                              body=message + "\nPhone: " + phone)
        except Exception as e:
            print("Error sending email:", e)

        return redirect('/contact')

    return render_template('shop/contact.html', params=params)


if __name__ == '__main__':
    app.run(debug=True)
