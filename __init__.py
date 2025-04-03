from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'ThisIsVerySecret'
    from .views import views #importing variable views from views.py
    from .auth import auth 
    app.register_blueprint(views, urlprefix ='/')
    app.register_blueprint(auth, urlprefix ='/') #no prefix needed to access route
    
    return app

