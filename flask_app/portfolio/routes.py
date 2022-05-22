from flask import (render_template, url_for,
                    flash, redirect,
                    request, abort,
                    Blueprint)
from flask_app import db, bcrypt
from flask_app.portfolio.forms import PostPortfolioForm
from flask_app.models import User, Portfolio_Post, Portfolio_Page_Update
from flask_app.portfolio.utils import save_portfolio_picture
from flask_login import  current_user, login_required

portfolio_bp = Blueprint('portfolio_bp', __name__)

### View the Portfolio, currently user needs to be logged in, remove if having this feature open to the public ###
@portfolio_bp.route("/portfolio")
@login_required
def portfolio():
    page_update = Portfolio_Page_Update.query.order_by(Portfolio_Page_Update.date_posted.desc()).first()
    page = request.args.get('page', 1, type=int)
    posts = Portfolio_Post.query.order_by(Portfolio_Post.date_posted.desc()).paginate(page=page, per_page=12)
    return render_template('portfolio.html', posts=posts, page_update=page_update)


### Post to the Portfolio ###
@portfolio_bp.route("/Portfolio_Post/new", methods=['GET', 'POST'])
@login_required
def new_portfolio_post():
    form = PostPortfolioForm()
    if form.validate_on_submit():
        picture_saved = save_portfolio_picture(form.portfolio_picture.data)
        post = Portfolio_Post(title=form.title.data,
                            portfolio_picture=picture_saved,
                            content=form.content.data,
                            author=current_user)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('portfolio_bp.portfolio'))
    return render_template('post_update_portfolio.html', title='New Image Post',form=form, legend='New Image Post')



@portfolio_bp.route("/portfolio_post/<int:post_id>")
def portfolio_by_id(post_id):
    post = Portfolio_Post.query.get_or_404(post_id)
    return render_template('portfolio_by_id.html', title=post.title, post=post)


@portfolio_bp.route("/Portfolio_Post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_portfolio_post(post_id):
    # making sure the post is real or sends user to 404 page
    post = Portfolio_Post.query.get_or_404(post_id)

    # making sure the person posting is the actual author
    # 403 is forbidden route
    if post.author != current_user:
        abort(403)
    form = PostPortfolioForm()

    # making sure the logic for form submission (updating) is good
    if form.validate_on_submit():
        # then we just update our post
        picture_saved = save_portfolio_picture(form.portfolio_picture.data)
        post.title = form.title.data
        post.portfolio_picture = picture_saved
        post.content = form.content.data
        db.session.commit()

        # flashing a message letting the user know that the post has been updated
        flash('Your post has been updated!', 'success')
        # this redirects the user back to the post they just updated
        # notice how the post_id is retreived
        return redirect(url_for('portfolio_bp.portfolio_by_id', post_id=post.id))


    # populating the title and content of the post that you want to update
    # (this way it's not deleting the previous post, just allowing the user
    # to update it)
    # we'll "only" display this if the request is a 'GET' request
    # (which technically it will be everytime until is a 'POST' so this
    # looks like it's more for structure and logic)
    elif request.method == 'GET':
        form.title.data = post.title
        form.portfolio_picture.data = post.portfolio_picture
        form.content.data = post.content

    # notice how the return render_template is always pushed first,
    # then all the if/else get run (this is the same in every route, python
    # indentation is why it's noticeable, how would it be done in C+ or JS?)
    return render_template('post_update_portfolio.html', title="Update Post",
                            form=form, legend='Update Post')

# -- Delete route --
@portfolio_bp.route("/Portfolio_Post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_portfolio_post(post_id):
    post = Portfolio_Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # adding deletion of post to the database session
    db.session.delete(post)
    # commiting the deletion
    db.session.commit()
    # flash message telling user the post has been delete
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main_bp.home'))
