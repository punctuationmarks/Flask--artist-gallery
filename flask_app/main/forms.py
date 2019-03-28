from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError



### Bio Page Form ###
class BioPageForm(FlaskForm):
    title = StringField('Title for Bio Page ', validators=[DataRequired()])
    content = TextAreaField('Body of Bio Page ', validators=[DataRequired()])
    bio_photo = FileField('Bio Photo (not required) ', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post Bio Page')

### Home Page Form ###
class HomePageForm(FlaskForm):
    title = StringField('Title for Home Page', validators=[DataRequired()])
    content = TextAreaField('Body of Home Page', validators=[DataRequired()])
    main_photo = FileField('Main Background Photo', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post Home Page')


### CUSTOMER INQUIRY FORM ###
class CustomerMessageForm(FlaskForm):
    customer_name = StringField('Name', validators=[DataRequired("Please enter your name")])
    customer_email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email()])
    customer_phone = StringField('Phone Number', validators=[Length(min=7, max=15)])
    customer_message = TextAreaField('Message', validators=[DataRequired("Please enter your message")])
    customer_submit = SubmitField('Send Message')

class GalleryForm(FlaskForm):
    title = StringField('Enter the gallery title', validators=[DataRequired("Enter the 'gallery' title")])
    subtitle = StringField('Subtitle Title')
    submit = SubmitField('Update Gallery Page')

class PortfolioForm(FlaskForm):
    title = StringField('Enter the Portfolio title', validators=[DataRequired("Enter the 'gallery' title")])
    subtitle = StringField('Subtitle Title')
    submit = SubmitField('Update Portfolio Page')

class StyleForm(FlaskForm):
    pass
