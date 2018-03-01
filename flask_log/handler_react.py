

from flask import render_template,request, jsonify, Response
from model import Trader,User
from flask_login import login_user,login_required,current_user,logout_user#in_manager


def run_app(app,login_manager):
    @app.route('/')
    def home():
        return "Home"

    @app.route('/register',methods=["GET","POST"])
    def register():

        if request.method == 'POST':
            data=request.form
            try:
                query= Trader.get(name=data['name'])
                print("User exists")
            except:
                Trader.create(name=data['name'], account=data['account'], password=data['password'])
                print("Record created")


        return render_template('register.html')



    @app.route('/login',methods=["POST"])
    def login():
#        pdb.set_trace()
        result=''
        print(request)
        data=request.get_json()
        print(data)
        username= data['name']
        print(username)
        userpassword = data['password']
        print(userpassword)
        dbname=None
        try: # Peewee returns an error if record not exist instead of returning none(!)
            dbname=Trader.get(name=username)
        except:
            pass
        if dbname:
            if dbname.password==userpassword:
                print("authenticated")
                user = get_user(dbname.id) # creates a User instance with id=id
                login_user(user)
                result="authenticated"
            else:
                print("wrong password")
                result="fail"
        else:
            print("Wrong Username")
            result="fail"
        print(result)
        return jsonify({"status":result})

#        return render_template('login.html')

    @app.route('/protected')
    @login_required
    def protected():
        return jsonify({"status":"Protected"})

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return Response('<Why access is denied string goes here...>', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})#jsonify({"status":"Unauthorized"})

    def get_user(id):
        try:
            dbuser=Trader.get(id=int(id))
            return User(dbuser.id)
        except:
            return None

    def hello():
        print("hello")

    @login_manager.user_loader
    def user_loader(id):
        return get_user(id)



    @app.route('/logout',methods=["GET","POST"])
    def logout():
        logout_user()
        return jsonify({"status":"Logged out"})



    return app


'''        @login_manager.request_loader
        def request_loader(request):
            try:
                query = Trader.get(name=request.form['name'])
                user=get_user(query.id)
                    # DO NOT ever store passwords in plaintext and always compare password
                    # hashes using constant-time comparison!
                user.is_authenticated = request.form['password'] == query.password
            except:
                user=None

                return user'''
