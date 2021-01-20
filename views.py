from flask import Flask, render_template, request, redirect, flash, url_for
import psycopg2 as dbapi2
from models import User, Rating, Movie
from database import Database
from forms import SigninForm, SignUpForm, AdminMovieAddForm, AddFriendForm, AdminMovieUpdateForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


def sign_in():
    form = SigninForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        database = Database()
        user_id = database.get_user_id(username)
        user = database.get_user(user_id)
        database = Database()
        if(username and password):
            if(user.password):
                if(database.verify_user(password, user.password)):
                    login_user(user)
                    flash("You have logged in.", "primary")
                    return redirect("/home_page")
            flash("Invalid credentials.", "danger")
    return render_template("signin.html", form=form)


@login_required
def sign_out():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for("sign_in"))


def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        birthday = form.birthday.data
        email = form.email.data
        if "@" not in email:
            flash("Invalid email", "danger")
        database = Database()
        print(username, password, birthday, email)
        user = User(0, username, password, birthday, email)
        database.add_user(user)
        next_page = request.args.get("next", url_for("sign_in"))
        return redirect(next_page)
    return render_template("signup.html", form=form)


@ login_required
def profile():
    user_id = current_user.get_id()
    database = Database()
    favorite_movies = database.get_all_favorite_movies(user_id)
    rated_movies = database.get_all_rated_movies(user_id)
    return render_template("profile.html", favorite_movies=favorite_movies, rated_movies=rated_movies)


@ login_required
def add_friend():
    user_id = current_user.get_id()
    database = Database()
    form = AddFriendForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        friends_username = form.friend_username.data
        try:
            database.add_friend(user_id, friends_username)
        except:
            flash("You entered wrong username", "danger")
    friends = database.get_all_friends(user_id)
    return render_template("add_friend.html", form=form, friends=friends)


@ login_required
def friends():
    user_id = current_user.get_id()
    database = Database()
    database.create_admin()
    database.create_admin_added()
    friends = database.get_all_friends(user_id)
    return render_template("friends.html", friends=friends)


@ login_required
def user_profile(username):
    database = Database()
    user_id = database.get_user_id(username)
    favorite_movies = database.get_all_favorite_movies(user_id)
    rated_movies = database.get_all_rated_movies(user_id)
    return render_template("profile.html", favorite_movies=favorite_movies, rated_movies=rated_movies)


def movie_details(movie_id):
    user_id = current_user.get_id()
    is_logged_in = user_id != None
    database = Database()
    movie = database.get_movie(movie_id)
    is_favorite = database.is_movie_favorite(user_id, movie_id)
    rating_obj = database.get_rating(user_id, movie_id)
    is_rated = rating_obj != None
    rating_value = rating_obj.user_rating if is_rated else None
    if request.method == 'POST':
        change_favorite = request.form.get("change_favorite")
        if change_favorite:
            if is_favorite:
                database.delete_favorite(user_id, movie_id)
            else:
                database.add_favorite(user_id, movie_id)
            is_favorite = not is_favorite
        rating = request.form.get("rating")
        if rating:
            rating = int(rating)
            if is_rated:
                database.update_rating(Rating(user_id, movie_id, rating))
            else:
                database.add_rating(Rating(user_id, movie_id, rating))
            rating_value = rating
            database.update_movie_rating(movie_id)
    return render_template("movie_details.html", movie=movie, is_logged_in=is_logged_in, is_favorite=is_favorite, is_rated=is_rated, rating_value=rating_value)


@ login_required
def admin_page():
    user_id = current_user.get_id()
    database = Database()
    if not database.is_user_admin(user_id):
        flash("You have to be an admin to enter", "danger")
        return redirect("/")

    form = AdminMovieAddForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        movie_title = form.movie_title.data
        movie_description = form.movie_description.data
        movie_image = form.movie_image.data
        admin_id = database.get_admin_id(user_id)
        database.add_movie(
            Movie(0, movie_title, movie_description, movie_image, None), admin_id)
    return render_template("admin_page.html", form=form)


@ login_required
def delete_movie(movie_id):
    user_id = current_user.get_id()
    if request.method == 'POST':
        movie_title = form.movie_title.data
        movie_description = form.movie_description.data
        movie_image = form.movie_image.data
        database = Database()
        if database.is_user_admin(user_id):
            database.delete_movie(movie_id)
    return redirect("/")


@ login_required
def update_movie(movie_id):
    user_id = current_user.get_id()
    form = AdminMovieUpdateForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        movie_title = form.movie_title.data
        movie_description = form.movie_description.data
        movie_image = form.movie_image.data
        database = Database()
        database.update_movie(
            Movie(movie_id, movie_title, movie_description, movie_image, None))
    return render_template("admin_page.html", form=form)


def movies_page():
    user_id = current_user.get_id()
    is_logged_in = user_id != None
    database = Database()
    if is_logged_in:
        is_admin = database.is_user_admin(user_id)
    movies = database.get_all_movies()
    return render_template("index.html", movies=movies, is_logged_in=is_logged_in, is_admin=is_admin)
