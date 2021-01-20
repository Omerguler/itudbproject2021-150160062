from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password, birthday, email):
        self.id = id
        self.username = username
        self.password = password
        self.birhday = birthday
        self.email = email
        self.active = True

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self.active


class Movie:
    def __init__(self, id, movie_title, movie_description, movie_image, movie_rating, is_favorited=False):
        self.id = id
        self.movie_title = movie_title
        self.movie_description = movie_description
        self.movie_image = movie_image
        self.movie_rating = movie_rating
        self.is_favorited = is_favorited

    def get_short_movie_description(self):
        if len(self.movie_description) > 100:
            return self.movie_description[:100] + "..."
        return self.movie_description


class Friend:
    def __init__(self, friend_id, username):
        self.friend_id = friend_id
        self.username = username


class Rating:
    def __init__(self, user_id, movie_id, user_rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.user_rating = user_rating


class MovieWithRating:
    def __init__(self, movie_id, movie_title, rating):
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.rating = rating
