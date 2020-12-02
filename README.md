# Flask artist-gallery

### Simple customizeable web app built in Python's Flask microframework, with SQLAlchemy and SQLite3 for the database, and with Bootstrap4 on the front end. It also usess Google's maps' API and Pillow for image resizing. 

It's a simple design to help local artists share, promote, express and sell their work. The design is meant to allow for customization while not taking away from the art itself. The site has a section for displaying art for sale (/Gallery), section for displaying artwork throughout the artist's career (/Portfolio), and section for the artist to write about whatever they would like (some small features, like the date stamp, are not shown to the viewer, only the artist, due to request). There is also a contact page and a Google map for client navigation if the artist has a physical shop. 
If you have any questions or want to get this up and running, let me know. 

The design of the app is very modular, similar to how Django would structure it's different "apps". Each feature in the app can be removed fairly easily without breaking anything, leaving it to be quite customizable. 



To have it run out of the box, you'll need to add your specific enviornment variables in /config.py

To install and develop on local machine:
```
$ python3 -m venv venv # create virtual environment, named "venv"
$ source venv/bin/activate # activating the virtual environment
$ pip3 install -r requirements.rxr # installing all requirements recursively
$ python3 run.py flask_app/ # running the app locally
```

Here's a [heroku](https://flask-artist-crud.herokuapp.com/) deployed version if you want to check it out. 
