import os
from app import create_app, db
from app.models import User, Contact, Phone

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#import dict to flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Contact=Contact, Phone=Phone)

if __name__ == "__main__":
    app.run(host="localhost", port="8080")
