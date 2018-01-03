import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_login import LoginManager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
#manager.add_command('db')

if __name__ == "__main__":
    manager.run()
