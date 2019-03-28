from flask_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

"""
database not being built? in terminal:
>>> from flask_app import create_app
>>> app = create_app()
>>> app.app_context().push()

Then "initialize" the database
>>> from flask_app import db
>>> db.drop_all()
>>> db.create_all()
"""
