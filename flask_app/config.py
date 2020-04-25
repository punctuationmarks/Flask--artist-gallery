import os

class Config:
    SECRET_KEY =  "ENTER_SECRET_KEY_HERE" #  os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' #os.environ.get('SQLALCHEMY_DATABASE_URI')
    # you can set key as config
    GOOGLEMAPS_KEY =  "ENTER_SECRET_KEY_HERE" # os.environ.get('GOOGLEMAPS_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "SOMETHING@GMAIL.COM" # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = "SOMETHINGTOUGHANDMEMORABLE" # os.environ.get('MAIL_PASSWORD')