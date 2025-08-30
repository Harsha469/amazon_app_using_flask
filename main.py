
from amazon_app import app,db
from amazon_app import views


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

# def top_decorator(func1):
#     print('second enters in this decorator')
#     def wrapper_one(*args, **kwargs):
#         result = func1(*args, **kwargs)
#
#     return wrapper_one
#
#
#
# def decorator(func):
#     print('first enters in this decorator')
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#
#     return wrapper
#
#
# @top_decorator
# @decorator
# def newone(name):
#     print('hello',name)
#
# #newone = decorator(newone)
# #newone = wrapper
# #new_one = top_decorator(wrapper)
# #new_one=wrapper_one
#
#
# newone('harsha')



# https://github.com/Harsha469/amazon_app_using_flask.git