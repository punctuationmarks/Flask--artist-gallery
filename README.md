# Flask artist-gallery

### Simple customizeable web app built in Python's Flask microframework, with SQLAlchemy and SQLite3 for the database, and with Bootstrap4 on the front end. It also usess Google maps' API and Pillow for image resizing. 

It's a simple design to help local artists share, promote, express and sell their work. The design is meant to allow for customization while not taking away from the art itself. The site has a section for displaying art for sale (Gallery), section for displaying artwork throughout the artist's career (Portfolio), and section for the artist to write about whatever they would like (small features, like the date stamp, are not shown to the viewer, only the artist, due to request). There is also a contact page and a Google map for client navigation. 
If you have any questions or want to get this up and running, let me know. 


To have it run out of the box, you'll need to add your specific enviornment variables in /config.py


To install and develop on local machine:
```
$ python3 -m venv venv # create virtual environment
$ pip3 install -r requirements.rxr # installing all requirements recursively
$ python3 run.py flask_app/
```

Here's a (heroku)[https://flask-artist-crud.herokuapp.com/] deployed version if you want to check it out. 
