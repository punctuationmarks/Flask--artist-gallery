from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_app import db, bcrypt
from flask_app.blog.forms import PostBlogForm
from flask_app.models import User, Blog_Post
from flask_login import login_required, current_user


blog_bp = Blueprint('blog_bp', __name__)


### View Blog ###
@blog_bp.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Blog_Post.query.order_by(Blog_Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts)


## post new blog post ##

@blog_bp.route("/Blog_Post/new", methods=['GET', 'POST'])
@login_required
def new_blog_post():
    form = PostBlogForm()
    if form.validate_on_submit():
        post = Blog_Post(title=form.title.data,
                        content=form.content.data,
                        author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog_bp.blog'))
    return render_template('post_update_blog.html',
                            title='New Post',
                            form=form,
                            legend='New Post')


### Route for every blog post to have unique page ###
@blog_bp.route("/Blog_Post/<int:post_id>")
def blog_by_id(post_id):
    post = Blog_Post.query.get_or_404(post_id)
    return render_template('blog_by_id.html', title=post.title, post=post)


## Update Blog Posts ##

@blog_bp.route("/Blog_Post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_blog_post(post_id):
    # making sure the post is real or sends user to 404 page
    post = Blog_Post.query.get_or_404(post_id)

    # making sure the person posting is the actual author
    # 403 is forbidden route
    if post.author != current_user:
        abort(403)
    form = PostBlogForm()

    # making sure the logic for form submission (updating) is good
    if form.validate_on_submit():
        # then we just update our post
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('blog_bp.blog_by_id', post_id=post.id))


    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('post_update_blog.html', title="Update Post",
                            form=form, legend='Update Post')

# -- Delete route --
# only accepting POST requests since
# this will be only shown on the delete post modal
@blog_bp.route("/Blog_Post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_blog_post(post_id):
    post = Blog_Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # adding deletion of post to the database session
    db.session.delete(post)
    # commiting the deletion
    db.session.commit()
    # flash message telling user the post has been delete
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main_bp.home'))




@blog_bp.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Blog_Post.query.filter_by(author=user)\
        .order_by(Blog_Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    return render_template('user_posts.html', posts=posts, user=user)
