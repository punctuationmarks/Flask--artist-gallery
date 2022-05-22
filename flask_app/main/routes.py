from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_mail import Message
from flask_app import db, bcrypt, mail
from flask_app.main.forms import (HomePageForm, BioPageForm, CustomerMessageForm)
from flask_app.main.utils import save_home_photo, save_bio_photo
from flask_app.models import (User, Blog_Post,
                            Home_Post, Bio_Post,
                            Gallery_Post, Customer_Message)
from flask_app.main.forms import GalleryForm
from flask_app.models import Gallery_Page_Update
from flask_login import current_user, login_required

main_bp = Blueprint('main_bp', __name__)


@main_bp.route("/")
@main_bp.route("/home")
def home():
    home_update = Home_Post.query.order_by(Home_Post.date_posted.desc()).first()
    return render_template('home.html', home_update=home_update)


@main_bp.route("/home/edit", methods=['GET', 'POST'])
@login_required
def update_home_page():
    post = Home_Post.query.order_by(Home_Post.date_posted.desc()).first()
    form = HomePageForm()
    if form.validate_on_submit():
        main_photo_saved = save_home_photo(form.main_photo.data)
        post = Home_Post(title=form.title.data,
                        content= form.content.data,
                        main_photo=main_photo_saved,
                        author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Home Page has been updated', 'success')
        return redirect(url_for('main_bp.home'))
    elif request.method == 'GET':
        if post:
            form.title.data = post.title
            form.content.data = post.content
            form.main_photo.data = post.main_photo
        else:
            form.title.data = "Home"
            form.content.data = "Lorem Ipsum"
            form.main_photo.data = "/static/home_photos/default.jpg"

    return render_template("home_edit.html",
                            title="Home Page Edit",
                            form=form,
                            legend='Home Page Edit')


@main_bp.route("/bio")
def bio():
    bio_update = Bio_Post.query.order_by(Bio_Post.date_posted.desc()).first()
    return render_template('bio.html', title='Bio', bio_update=bio_update)

@main_bp.route("/bio/edit", methods=['GET', 'POST'])
@login_required
def update_bio_page():
    post = Bio_Post.query.order_by(Bio_Post.date_posted.desc()).first()
    form = BioPageForm()
    if form.validate_on_submit():
        bio_photo_saved = save_bio_photo(form.bio_photo.data)
        post = Bio_Post(title=form.title.data,
                        content=form.content.data,
                        bio_photo=bio_photo_saved,
                        author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your bio Page has been updated', 'success')
        return redirect(url_for('main_bp.bio'))
    elif request.method == 'GET':
        if post:
            form.title.data = post.title
            form.content.data = post.content
            form.bio_photo.data = post.bio_photo

        else:
            form.title.data = "Bio"
            form.content.data = "Lorem Ipsum"
            form.bio_photo.data = "/static/bio_photos/default.jpg"

    return render_template("bio_edit.html",
                            title="Bio Page Edit",
                            form=form,
                            legend='Bio Page Edit')


@main_bp.route("/gallery/update_gallery", methods=['GET', 'POST'])
@login_required
def update_gallery():
    legend = "Gallery"
    post = Gallery_Page_Update.query.order_by(Gallery_Page_Update.date_posted.desc()).first()
    form = GalleryForm()
    if form.validate_on_submit():
        post = Gallery_Page_Update(title=form.title.data,
                            subtitle=form.subtitle.data,
                            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Gallery Page has been updated', 'success')
        return redirect(url_for('gallery_bp.gallery'))
    elif request.method == 'GET':
        if post:
            form.title.data = post.title
            form.subtitle.data = post.subtitle
        else:
            form.title.data = "Gallery"
            form.subtitle.data = "Subtitle..."

    return render_template("gallery_portfolio_edit.html",
                            title="Gallery Page Edit",
                            form=form, legend=legend)


@main_bp.route("/portfolio/update_portfolio", methods=['GET', 'POST'])
@login_required
def update_portfolio():
    legend = "Portfolio"
    post = Portfolio_Page_Update.query.order_by(Portfolio_Page_Update.date_posted.desc()).first()
    form = PortfolioForm()
    if form.validate_on_submit():
        post = Portfolio_Page_Update(title=form.title.data,
                            subtitle=form.subtitle.data,
                            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Portfolio Page has been updated', 'success')
        return redirect(url_for('portfolio_bp.portfolio'))
    elif request.method == 'GET':
        if post:
            form.title.data = post.title
            form.subtitle.data = post.subtitle
        else:
            form.title.data = "portfolio"
            form.subtitle.data = "Subtitle..."

    return render_template("gallery_portfolio_edit.html",
                            title="portfolio Page Edit",
                            form=form, legend=legend)
