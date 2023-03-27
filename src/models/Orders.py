from src.config.mysqlconnection import connectToMySQL
from src import app
from flask import flash
from datetime import datetime

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Order:
    db_name = 'maintenance'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.date = db_data['date']
        self.last_name = db_data['time']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.technician_id = db_data['technician_id']
        self.costumer_id = db_data['costumer_id']
        self.admin_id = db_data['admin_id']

    @classmethod
    def get_all(cls):
        query = "SELECT orders.id, orders.date, orders.time, orders.created_at,\
                orders.updated_at, users.first_name,orders.technician_id,orders.open,costumers.nickname,\
                costumers.address, costumers.num, users.last_name, costumers.state, costumers.contact_name,\
                costumers.email, users.first_name, orders.open, orders.delete_admin FROM orders LEFT JOIN costumers ON orders.costumer_id = costumers.id\
                LEFT JOIN users ON technician_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(user)
        return users
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user

    @classmethod
    def get_one_order_in_admin(cls,data):
        query = "SELECT * FROM orders LEFT JOIN costumers ON orders.costumer_id = costumers.id WHERE orders.id = %(id)s; "
        results = connectToMySQL(cls.db_name).query_db(query,data)
        order_in_admin = []
        for user in results:
            order_in_admin.append(user)
        return order_in_admin

# ----------- All Orders Assignment ----------------
    @classmethod
    def get_order_assignment(cls):
        query = "SELECT orders.id, costumers.nickname, users.first_name, users.last_name, orders.delete_admin, orders.open FROM orders LEFT JOIN costumers ON costumer_id = costumers.id \
                LEFT JOIN users ON technician_id = users.id WHERE orders.open = 1 AND orders.delete_admin = 1;"
        results = connectToMySQL(cls.db_name).query_db(query)
        orders = []
        for result in results:
            orders.append(result)
        return orders

    
#  -----------Only orders assignment a Technicians----------------


    @classmethod
    def only_assigment_by_tech(cls,data):
        query ="SELECT orders.id, costumers.nickname, orders.date, orders.time, users.first_name, users.last_name, orders.open, orders.delete_admin, \
                costumers.id AS costumer_id FROM orders LEFT JOIN costumers on costumer_id = costumers.id LEFT JOIN users ON technician_id = users.id \
                where technician_id = %(id)s AND orders.open = 1 and orders.delete_admin = 1;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        orders = []
        for user in results:
            orders.append(user)
        return orders

#------------- Create order---------------------------------


    @classmethod
    def create_order(cls,data):
        query = "INSERT INTO orders (date,time,created_at,updated_at,technician_id, costumer_id, admin_id, open, delete_admin) VALUES(%(date)s,%(time)s,NOW(),NOW(),%(technician_id)s, %(costumer_id)s, %(admin_id)s, 1, 1);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results


# --------------close orders-----------------------------

    @classmethod
    def close_order(cls,data):
        query = "UPDATE orders SET orders.open = 0 WHERE orders.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results
    
    @classmethod
    def close_order_by_admin(cls,data):
        query = "UPDATE orders SET orders.delete_admin = 0 WHERE orders.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results



