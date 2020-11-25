from Projectapi import db

class User(db.Model):
    id = db.Column( db.Integer , primary_key = True)
    email = db.Column( db.String(100), unique = True, nullable = False)
    password =db.Column( db.String(80), nullable = False)
    first_name =db.Column( db.String(80), nullable = False)
    last_name = db.Column( db.String(80), nullable = False)
    is_admin = db.Column( db.Boolean, nullable = False, default = False)

    def __init__(self,email,password,first_name,last_name,is_admin):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def Jsonify(self):
        return{
            'id': self.id,
            'email':self.email,
            'password':self.password,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'is_admin':self.is_admin
        }
    

class Category(db.Model):
    id = db.Column( db.Integer , primary_key = True)
    title = db.Column( db.String(200), unique = True,nullable = False)

    def __init__(self,title):
        self.title = title

    def Jsonify(self):
        return{
            'id':self.id,
            'title':self.title
        }
