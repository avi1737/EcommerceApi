from Projectapi.Models import User
from flask import Flask, request,jsonify,url_for
from Projectapi import app
from flask_mail import Message
from Projectapi import mail, db
from Projectapi.utils import generate_confirmation_token,confirm_token
from random import randint

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
    email = request.args.get('email')
    password = request.args.get('password')

    user = User.query.filter_by( email = email).first()
    if user is not None and user.password == password:
        result = { 'message': "success"}
    else:
        result = { 'message': 'user not found'}

    return result

