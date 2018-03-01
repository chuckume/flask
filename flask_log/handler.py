

from flask import render_template,request
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



    @app.route('/login',methods=["GET","POST"])
    def login():
#        pdb.set_trace()
        if request.method == 'POST':
            data=request.form
            username= data['name']
            userpassword = data['password']
            dbname=None
            try: # Peewee returns an error if record not exist instead of returning none(!)
                dbname=Trader.get(name=username)
            except:
                pass
            if dbname:
                if dbname.password==userpassword:
                    print("Authenticated")
                    user = get_user(dbname.id) # creates a User instance with id=id
                    login_user(user)
                    result="authenticated"
                else:
                    print("Wrong password")
                    result="fail" # Should always return fail regardless if its password or username
            else:
                print("Wrong Username")
                result="fail"# Should always return fail regardless if its password or username
        return render_template("login.html")

#        return render_template('login.html')

    @app.route('/protected')
    @login_required
    def protected():
        return 'Logged in as: ' + str(current_user.id)

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return 'Unauthorized'

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
        return 'Logged out'



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
