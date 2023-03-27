from src.config.mysqlconnection import connectToMySQL
from src import app
from flask import flash
from datetime import datetime

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = 'maintenance'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.is_admin = db_data['is_admin']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def get_all_tech(cls):
        query = "SELECT * FROM users WHERE is_admin = 0;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_all_admin(cls):
        query = "SELECT * FROM users WHERE is_admin = 1;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user
    

    # Create Admins
    @classmethod
    def save_admin(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,is_admin,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,1,NOW(),NOW())"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results
    

    # Create Technicians
    @classmethod
    def save_tech(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,is_admin,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,0,NOW(),NOW())"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results    

    # Validate User

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM Users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Confirm Passwords don't match","register")
            is_valid= False
        return is_valid