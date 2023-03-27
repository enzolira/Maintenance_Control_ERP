from src.config.mysqlconnection import connectToMySQL
from src import app
from flask import flash
from datetime import datetime

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Costumer:
    db_name = 'maintenance'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.nickname = db_data['nickname']
        self.address = db_data['address']
        self.num = db_data['num']
        self.state = db_data['state']
        self.contact_name = db_data['contact_name']
        self.email = db_data['email']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.active = db_data['active']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM costumers WHERE costumers.active = 1;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM costumers WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user

    @classmethod
    def get_id_costumer(cls):
        costumers = Costumer.get_all()
        costumer_ids = [costumer.id for costumer in costumers]
        return costumer_ids


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM costumers WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user
    

    # Create Costumer
    @classmethod
    def save(cls,data):
        query = "INSERT INTO costumers (nickname,address,num,state,contact_name,email,created_at,updated_at, active) VALUES(%(nickname)s,%(address)s,%(num)s,%(state)s,%(contact_name)s,%(email)s,NOW(),NOW(), 1);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results
    
    # delete costumer
    @classmethod
    def delete_costumer(cls, data):
        query ="UPDATE costumers SET costumers.active = 0 WHERE costumers.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    # Validate Costumer

    @staticmethod
    def validate_client(user):
        is_valid = True
        query = "SELECT * FROM costumers WHERE email = %(email)s;"
        results = connectToMySQL(Costumer.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['nickname']) < 3:
            flash("Address must be at least 3 characters","register")
            is_valid= False
        if len(user['address']) < 3:
            flash("Address must be at least 3 characters","register")
            is_valid= False
        if len(user['num']) > 5:
            flash("N° must be 5 characters maximum","register")
            is_valid= False
        if len(user['state']) < 3:
            flash("Address must be at least 3 characters","register")
            is_valid= False
        if len(user['contact_name']) < 2:
            flash("Name must be at least 2 characters","register")
            is_valid= False
        return is_valid
