
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_app import db, bcrypt
from flask_app.gallery.forms import PostGalleryForm
from flask_app.gallery.utils import save_gallery_picture
from flask_app.models import Gallery_Post
from flask_login import current_user, login_required

# TESTING #
from flask_app.models import Gallery_Page_Update

gallery_bp = Blueprint('gallery_bp', __name__)


@gallery_bp.route("/gallery")
def gallery():
    page_update = Gallery_Page_Update.query.order_by(Gallery_Page_Update.date_posted.desc()).first()
    page = request.args.get('page', 1, type=int)
    posts = Gallery_Post.query.order_by(Gallery_Post.date_posted.desc()).paginate(page=page, per_page=12)
    return render_template('gallery.html', posts=posts, page_update=page_update)



@gallery_bp.route("/gallery_Post/new", methods=['GET', 'POST'])
@login_required
def new_gallery_post():
    form = PostGalleryForm()
    if form.validate_on_submit():
        picture_saved = save_gallery_picture(form.gallery_picture.data)
        post = Gallery_Post(title=form.title.data,
                            gallery_picture=picture_saved,
                            content=form.content.data,
                            price=form.price.data,
                            author=current_user)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('gallery_bp.gallery'))
    return render_template('post_update_gallery.html', title='New Image Post',form=form, legend='New Image Post')



@gallery_bp.route("/gallery_post/<int:post_id>")
def gallery_by_id(post_id):
    post = Gallery_Post.query.get_or_404(post_id)
    return render_template('gallery_by_id.html', title=post.title, post=post)


@gallery_bp.route("/gallery_Post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_gallery_post(post_id):
    # making sure the post is real or sends user to 404 page
    post = Gallery_Post.query.get_or_404(post_id)

    # making sure the person posting is the actual author
    # 403 is forbidden route
    if post.author != current_user:
        abort(403)
    form = PostGalleryForm()

    # making sure the logic for form submission (updating) is good
    if form.validate_on_submit():
        # then we just update our post
        picture_saved = save_gallery_picture(form.gallery_picture.data)
        post.title = form.title.data
        post.gallery_picture = picture_saved
        post.content = form.content.data
        post.price = form.price.data
        db.session.commit()

        # flashing a message letting the user know that the post has been updated
        flash('Your post has been updated!', 'success')
        # this redirects the user back to the post they just updated
        # notice how the post_id is retreived
        return redirect(url_for('gallery_bp.gallery_by_id', post_id=post.id))


    # populating the title and content of the post that you want to update
    # (this way it's not deleting the previous post, just allowing the user
    # to update it)
    # we'll "only" display this if the request is a 'GET' request
    # (which technically it will be everytime until is a 'POST' so this
    # looks like it's more for structure and logic)
    elif request.method == 'GET':
        form.title.data = post.title
        form.gallery_picture.data = post.gallery_picture
        form.content.data = post.content
        form.price.data = post.price

    # notice how the return render_template is always pushed first,
    # then all the if/else get run (this is the same in every route, python
    # indentation is why it's noticeable, how would it be done in C+ or JS?)
    return render_template('post_update_gallery.html', title="Update Post",
                            form=form, legend='Update Post')

# -- Delete route --
@gallery_bp.route("/gallery_Post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_gallery_post(post_id):
    post = Gallery_Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # adding deletion of post to the database session
    db.session.delete(post)
    # commiting the deletion
    db.session.commit()
    # flash message telling user the post has been delete
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main_bp.home'))
