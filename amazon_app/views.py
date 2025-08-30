from functools import wraps
from amazon_app import app,db
from amazon_app.models import ProductItems,UsersTable
from flask import jsonify,request,session
from werkzeug.security import generate_password_hash,check_password_hash
@app.route('/')
def home():
    return {'msg':'Home page'}


@app.route('/items/get_all', methods = ['GET'])
def get_all_items():
    data = ProductItems.query.all()
    if not data:
        return jsonify(msg='no data is found')
    result = []
    for each in data:
        result.append({'id':each.id,'product_name':each.name,'price':each.price})

    return jsonify(msg=result)


@app.route('/items/<int:id>', methods = ['GET'])
def get_one_item(id):
    data = ProductItems.query.get(id)

    if not data:
        return jsonify(msg=f'This product id {id} is not available')

    return jsonify(msg={'id':data.id,'name':data.name,'price':data.price})


@app.route('/items/<string:name>', methods=['GET'])
def get_product_name(name):
    data = ProductItems.query.filter(name==name).first()

    if not data:
        return jsonify(msg=f'This product name {name} is not available')

    return jsonify(msg={'id':data.id,'name':data.name,'price':data.price})


@app.route('/get_multiple', methods = ['GET'])
def get_multiple_items():

    data = request.args.to_dict()

    #get all valid column names for product items
    valid_columns = {col.name for col in ProductItems.__table__.columns}

    #checking the column names present in query params
    filter_keys = {k:v for k,v in data.items() if k in valid_columns}

    if not filter_keys:
        return jsonify(msg='provide query params then i can search the result for you '),400

    get_data = ProductItems.query.filter_by(**filter_keys).all()

    if not get_data:
        return jsonify(msg='no data is found the item you searched')

    elif len(get_data) == 1:
        first = get_data[0]
        return jsonify(msg = {'name':first.name,'price':first.price})

    elif len(get_data) > 1:
        result = [{'id':each.id,'name':each.name,'price':each.price} for each in get_data]
        return jsonify(msg=result)







@app.route('/add_items', methods = ['POST'])
def add_new_items():
    data = request.get_json(silent=True)


    #get all the column names in database product items table
    valid_columns = {col.name for col in ProductItems.__table__.columns if not col.primary_key}

    #check the user sending all the columns which are present in our database table
    missing_fields = valid_columns - data.keys()  #performing set operation

    if missing_fields:
        return jsonify(msg = f"Missing required fields: {', '.join(missing_fields)}")

    data = ProductItems(**data)
    db.session.add(data)
    db.session.commit()
    return jsonify(msg='Product added successfully')


    # if not data or 'name' not in data or 'price' not in data:
    #     return jsonify(msg='provide product name and price to add in amazon')
    #
    # new_product = ProductItems(name=data['name'], price=data['price'])
    # db.session.add(new_product)
    # db.session.commit()
    # return jsonify(msg='product is added successfully in to the database')


@app.route('/sign_up', methods = ['POST'])
def register_to_app():
    data = request.get_json(silent=True)

    if not data:
        return jsonify(msg='please provide user_name and password to register'), 400

    #required_columns
    # columns = {col.name for col in UsersTable.__table__.columns if not col.primary_key}
    columns = {'user_name','password'}

    #check user is providing both user_name and password while registering
    check = columns - data.keys()

    if check:
        return jsonify(msg=f"{', '.join(check)} is missing please provide it to register") , 400

    empty_fields = []
    for _ in columns:
        if not data.get(_).strip():
            empty_fields.append(_)

    if empty_fields:
        return jsonify(msg=f"{', '.join(empty_fields)} could not be empty"), 400

    is_user_name_present = UsersTable.query.filter_by(user_name=data['user_name']).first()

    if is_user_name_present:
        return jsonify(msg='This username is already taken') , 400


    data['password'] = generate_password_hash(data['password'])
    try:
        new_user = UsersTable(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(msg='Registered successfully', redirect_url = '/login'), 200
    except Exception as e:
        return {'msg':str(e)}

@app.route('/login', methods = ['POST'])
def user_login():
    data = request.get_json()

    #1 check whether user is providing any data or not

    if not data:
        return jsonify(msg='please provide user_name and password to login'), 400

    user_name = data.get('user_name').strip()
    password = data.get('password').strip()
    #checking required fields
    if not user_name or not password:
        return jsonify(msg="provide valid credentials"), 400

    #checking user is registered with us
    is_user = UsersTable.query.filter_by(user_name=user_name).first()

    #if user is not registered
    if not is_user:
        return jsonify(msg="register to login", redirect_url = '/sign_up'), 404

    #if user provides invalid password
    if not check_password_hash(is_user.password,password):
        return jsonify(msg='Invalid password'), 401

    session['user_name'] = user_name
    return jsonify(msg='login Success') , 200


    # # 2 check required fields
    # columns = {'user_name','password'}
    # check = columns - data.keys()
    #
    # if check:
    #     return jsonify(msg=f"Enter {', '.join(check)} "), 400
    #
    # # 3 check empty fields
    # empty_fields = []
    # for _ in columns:
    #     if not data.get(_).strip():
    #         empty_fields.append(_)
    #
    # if empty_fields:
    #     return jsonify(msg=f"provide valid {', '.join(empty_fields)} ")
    #
    # #query to database
    # is_user_present = UsersTable.query.filter_by(user_name=data['user_name']).first()
    #
    # if not is_user_present:
    #     return jsonify(msg='Invalid Credentials',redirect_url='/sign_up'), 404
    #
    # if not check_password_hash(is_user_present.password, data['password']):
    #     return jsonify(msg = 'Invalid Password') , 401
    #
    # return jsonify(msg = 'Login Successful'), 200
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session.get('user_name'):
            return jsonify(redirect_url = '/login')
        return func(*args,**kwargs)
    return wrapper





@app.route('/profile')
@login_required
def profile():
    return jsonify(msg = 'user can enter to profile page')

@app.route("/logout")
def logout():
    session.pop('user_name', None)   # remove user from session
    return jsonify(msg="You are logged out")


#400 bad request required fields missing the client
#401 unauthorized person registered with us but password is wrong
#404 not registered with us trying to login















