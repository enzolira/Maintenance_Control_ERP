from flask import Flask, render_template, redirect, request, session, flash
from src import app
from src.models.Users import User
from src.models.Costumers import Costumer
from src.models.Orders import Order
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

# ----------------START PAGE --------------------


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register_admin')
def register_admin():
    return render_template('register_admin.html')

@app.route('/add_costumer')
def add_costumer():

    if 'user_id' not in session:
        return redirect('/')

    return render_template('register_costumer.html')

@app.route('/register_tech')
def register_tech():

    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('register_tech.html')




# # -------- LOGIN PAGE--------------------





@app.route('/login',methods=['POST'])
def login_admin():

    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        flash("Email and password are required.", "login")
        return redirect('/')

    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')

    session['user_id'] = user.id

    if user.is_admin == 1:
        return redirect('/index_admin')
    else:
        return redirect('/index_technician')





#---------------ADMIN PAGE-------------------------





@app.route('/index_admin')
def user_admin():

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': session['user_id']
    }

    admin = User.get_one(data)
    clients = Costumer.get_all()
    orders = Order.get_order_assignment()
    print(orders)
    return render_template('admin.html', admin=admin, clients=clients, orders=orders, session=session)




# --------------detail clients--------------------------



@app.route('/detail/<int:id>')
def detail(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id':id
    }
    client = Costumer.get_one(data)

    return render_template('detail.html', client=client)





# --------------All Tech in Networks--------------------------




@app.route('/total_tech')
def total_tech():

    if 'user_id' not in session:
        return redirect('/')
    
    all_tech = User.get_all_tech()

    return render_template('all_tech.html', all_tech=all_tech)





# --------------All orders in Networks--------------------------





@app.route('/total_orders')
def total_order():

    if 'user_id' not in session:
        return redirect('/')
    
    total_orders = Order.get_all()
    return render_template('all_orders.html', total_orders=total_orders)

# ---------------Detail order ----------------------

@app.route('/order_show/<int:id>')
def show_order(id):
    
    if 'user_id' not in session:
        return redirect('/')
    
    data = { 'id': id}

    detail_order = Order.get_one_order_in_admin(data)
    return render_template('detail_order.html', detail_order=detail_order)

#  ------------ DELETE orders----------------------


@app.route('/delete_order/<int:id>')
def delete_order(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {'id': id}
    Order.close_order_by_admin(data)

    return redirect('/index_admin')


#  ------------ DELETE costumers----------------------


@app.route('/delete_costumer/<int:id>')
def delete_costumer(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {'id': id}
    Costumer.delete_costumer(data)

    return redirect('/index_admin')

#---------------TECHNICIAN PAGE-------------------------


@app.route('/index_technician')
def user_tech():

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': session['user_id']
    }

    tech = User.get_one(data)
    orders = Order.only_assigment_by_tech(data)

    return render_template('tech.html', tech=tech, orders=orders)


# --------------detail clients in tech--------------------------




@app.route('/show/<int:id>')
def detail_tech(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id':id
    }
    client = Costumer.get_one(data)

    return render_template('detail_tech.html', client=client)




# --------------close order in tech--------------------------





@app.route('/close/<int:id>')
def close_order(id,):

    data = {
        'id':id
    }

    Order.close_order(data)

    return redirect('/index_technician')





# -------------- Register ADMINS -----------------






@app.route('/add_admin', methods=['POST'])
def add_admin():


    if not all(request.form.values()):
        flash('Please fill out all fields.', 'register')
        return redirect('/register_admin')

    if not User.validate_register(request.form):
        return redirect('/register_admin')
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form["password"])
    }

    id = User.save_admin(data)
    session['user_id'] = id

    return redirect('/')





# ---------------Register TECHNICALS--------------





@app.route('/add_tech', methods=['POST'])
def add_tech():

    if 'user_id' not in session:
        return redirect('/')

    if not all(request.form.values()):
        flash('Please fill out all fields.', 'register')
        return redirect('/register_tech')

    if not User.validate_register(request.form):
        return redirect('/register_tech')
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form["password"])
    }

    User.save_tech(data)

    return redirect('/index_admin')





# ---------------Register CLIENTS--------------



@app.route('/add_client', methods=['POST'])
def add_client():

    if 'user_id' not in session:
        return redirect('/')
    

    if not all(request.form.values()):
        flash('Please fill out all fields.', 'register')
        return redirect('/add_costumer')

    if not Costumer.validate_client(request.form):
        return redirect('/add_costumer')
    
    data = {
        'nickname': request.form['nickname'],
        'address': request.form['address'],
        'num': request.form['num'],
        'state': request.form['state'],
        'contact_name': request.form['contact_name'],
        'email': request.form['email']
    }

    Costumer.save(data)

    return redirect('/index_admin')




# ---------------Register Order--------------




@app.route('/add_order/<int:id>')
def add_order(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id':id
    }

    technicians = User.get_all_tech()
    costumer = Costumer.get_one(data)
    admins = User.get_all_admin()

    return render_template('register_order.html', admins=admins, technicians=technicians, costumer=costumer)


@app.route('/assignment', methods=['POST'])
def new_order():

    if 'user_id' not in session:
        return redirect('/')

    if not all(request.form.values()):
        flash('Please fill out all fields.', 'register')
        return redirect('/add_order/'+ request.form['costumer_id'])

    if not request.form.get('technician_id'):
        flash('Please select a technician.', 'register')
        return redirect('/add_order/'+ request.form['costumer_id'])


    data = {
        'date': request.form['date'],
        'time': request.form['time'],
        'technician_id': request.form['technician_id'],
        'costumer_id': request.form['costumer_id'],
        'admin_id': request.form['admin_id'],
    }

    print(data)
    Order.create_order(data)
    
    return redirect('/index_admin')





# # -------- Logout -----------



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




#------------- API time, location and weather ---------------------


