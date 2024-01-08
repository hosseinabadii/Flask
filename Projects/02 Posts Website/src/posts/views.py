from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from main import services
from main.models import Post, User

from .froms import PostForm

posts = Blueprint(
    "posts",
    __name__,
    # static_folder="static",
    # static_url_path="/posts/static",
    # template_folder="templates",
)


@posts.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_public=form.is_public.data,
            author_id=current_user.id,
        )
        services.add(post)
        flash("Your post has been created!", "success")
        return redirect(url_for("posts.my_posts"))
    return render_template(
        "posts/create_update_post.html",
        form=form,
        title="New Post",
        legend="Create a new post",
    )


@posts.route("/<int:post_id>")
def post(post_id: int):
    post = services.get_or_404(Post, post_id)
    if (post.author != current_user) and (post.is_public is False):
        abort(403)
    return render_template("posts/post.html", post=post)


@posts.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id: int):
    post = services.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_public = form.is_public.data
        services.update()
        flash("Your post has been updated successfuly!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    form.is_public.data = post.is_public
    return render_template(
        "posts/create_update_post.html",
        form=form,
        title="Update Post",
        legend="Update the post",
    )


@posts.route("/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id: int):
    post = services.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    services.delete(post)
    flash("Your post has been deleted successfuly!", "success")
    return redirect(url_for("main.index"))


@posts.route("/my-posts")
@login_required
def my_posts():
    posts = current_user.posts
    return render_template("posts/my_posts.html", posts=posts)


@posts.route("/user/<username>")
def user_posts(username: str):
    user = services.get_first_or_404_filter_by(User, username=username)
    if user == current_user:
        return redirect(url_for("posts.my_posts"))
    return render_template("posts/user_posts.html", posts=user.posts)
