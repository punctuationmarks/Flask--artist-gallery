from flask_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

"""
# database not being built on run? in the virtual environment in python3's cli:
from flask_app import create_app
app = create_app()
app.app_context().push()

# initialize the database
from flask_app import db
db.drop_all()
db.create_all()
"""
