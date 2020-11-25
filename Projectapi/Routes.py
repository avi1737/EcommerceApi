from Projectapi.Models import User, Category
from flask import Flask, request,jsonify,url_for
from Projectapi import app
from flask_mail import Message
from Projectapi import mail, db
from Projectapi.utils import generate_confirmation_token,confirm_token
from random import randint
from sqlalchemy import exc

otp = randint(000000,999999)
otp = str(otp)

@app.route('/')
def get_users():
    users = User.query.all()
    return jsonify( users = [ user.Jsonify() for user in users])


@app.route('/auth/register/', methods = ['POST'])
def register_user():
    result = {}
    if User.query.filter_by(email = request.args.get('email')).first() != None:
        result = { 'user_present':True, 'message':"Email is already in use"}

    else:
        email = request.args.get('email')
        password = request.args.get('password')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        is_admin = False
        if request.args.get('is_admin') == 'true':
            is_admin = True
        msg = Message('Your verification link', sender = 'avinashvarpeti1@gmail.com', recipients = [email])
        """token = generate_confirmation_token(email)
        confirm_url = url_for('register_user', token=token, _external=True)
        msg.body = confirm_url"""
        msg.body = "Your One time password for FoodMart.io is :"+otp
        mail.send(msg)
        new_user = User(email,password,first_name,last_name,is_admin)
        db.session.add(new_user)
        db.session.commit()
        result = { 'message': 'User Registered Successfully'}

    return result

@app.route('/auth/register/otp/',methods = ['POST'])
def otp_verification():
    res = {}
    user_otp = request.form['otp']
    print(user_otp)
    print(otp)
    if otp == user_otp:
        res = { 'confirm': 'YES'}
    else:
        res = { 'confirm': 'NO' }
    return res


@app.route('/auth/login/',methods = ['POST'])
def login():
    result = {}
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(email)
    print(password)
    user = User.query.filter_by( email = email).first()
    if user is not None and user.password == password:
        if user.is_admin:
            result = { 'admin': True,
                       'message':'user found'
                    }
        else:
            result = { 'admin': False,
                       'message':'user found'
                     }
    else:
        result = { 'message': 'user not found'}

    return result

@app.route('/add/category/',methods = ['GET','POST'])
def add_category():
    result = {}
    res = request.get_json()
    title = res['title']
    try:
        new_category = Category(title = title)
        db.session.add(new_category)
        db.session.commit()
        result = { 'message':'success'}
    except exc.SQLAlchemyError as e:
        result = {'messgae':'failure','error':type(e)}
    return result

@app.route('/get/category/',methods = ['GET'])
def get_category():
    result = {}
    try:
        categories = Category.query.all()
        return jsonify( categories = [ category.Jsonify() for category in categories])
    except exc.SQLAlchemyError as e:
        result = { 'message':'failure'}
        return result

@app.route('/delete/category/<id>', methods = ['GET','DELETE'])
def delete_category():
    print(request.args.get('id'))
    try:
        category = Category.query.filter_by(id = id)
        db.session.delete(category)
        db.session.commit()
        result = { 'message': 'success'}
    except exc.SQLAlchemyError as e:
        result = { 'message': 'failure'}
        
    return result

        
