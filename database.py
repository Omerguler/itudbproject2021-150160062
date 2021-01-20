from flask import Flask
import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from models import User, Movie, Friend, MovieWithRating, Rating
import os


class CursorHelper:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def cursor_execute(self, sql_command, variables=""):
        with dbapi2.connect(self.connection_string) as connection:
            cursor = connection.cursor()
            if variables == "":
                cursor.execute(sql_command)
            else:
                cursor.execute(sql_command, variables)
            connection.commit()
            cursor.close()

    def cursor_fetch_one(self, sql_command, variables=""):
        with dbapi2.connect(self.connection_string) as connection:
            cursor = connection.cursor()
            if variables == "":
                cursor.execute(sql_command)
            else:
                cursor.execute(sql_command, variables)
            query_result = cursor.fetchone()
            connection.commit()
            cursor.close()

        return query_result

    def cursor_fetch_all(self, sql_command, variables=""):
        with dbapi2.connect(self.connection_string) as connection:
            cursor = connection.cursor()
            if variables == "":
                cursor.execute(sql_command)
            else:
                cursor.execute(sql_command, variables)
            query_result = cursor.fetchall()
            connection.commit()
            cursor.close()

        return query_result


class Database:
    def __init__(self):
        #self.connection_string = os.getenv("DATABASE_URL")
        self.connection_string = "postgres://cjiwqgiq:bBBKV8OjTd-pkOtBvcwAq-YX8yJBKd3i@kandula.db.elephantsql.com:5432/cjiwqgiq"
        self.cursor_helper = CursorHelper(self.connection_string)

    def get_user_id(self, username):
        sql_command = "SELECT ID FROM USERS WHERE(username = %(username)s)"
        variables = {"username": username}
        result = self.cursor_helper.cursor_fetch_one(
            sql_command=sql_command, variables=variables)
        if len(result) == 0:
            return None
        return result

    def get_user(self, user_id):
        sql_command = "SELECT * FROM USERS WHERE(ID = %(id)s)"
        variables = {"id": user_id}
        result = self.cursor_helper.cursor_fetch_one(
            sql_command=sql_command, variables=variables)
        if len(result) == 0:
            return None
        return User(*result)

    def create_user(self):
        sql_command = "CREATE TABLE IF NOT EXISTS USERS (ID SERIAL PRIMARY KEY ,USERNAME VARCHAR(100), PASSWORD VARCHAR(100), EMAIL VARCHAR(100), BIRTHDAY VARCHAR(100))"
        self.cursor_helper.cursor_execute(sql_command=sql_command)

    def add_user(self, user):
        sql_command = "INSERT INTO USERS (USERNAME,PASSWORD,EMAIL,BIRTHDAY) VALUES (%(username)s, %(password)s, %(email)s, %(birthday)s)"
        user.password = hasher.hash(user.password)
        variables = {'username': user.username, 'password': user.password,
                     'email': user.email, 'birthday': user.birhday}
        self.cursor_helper.cursor_execute(
            sql_command=sql_command, variables=variables)

    def add_admin(self, user_id):
        sql_command = "INSERT INTO ADMINS (USER_ID) VALUES ( USER_ID = %(user_id)s )"
        variables = {'user_id': user_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def get_hashed_password(self, name):
        sql_command = "SELECT PASSWORD FROM USERS WHERE(USER_NAME = %(user_name)s)"
        variables = {'user_name': name}
        return self.cursor_helper.cursor_fetch_one(
            sql_command=sql_command, variables=variables)

    def verify_user(self, password, hashed_password):
        return(hasher.verify(password, hashed_password))

    def create_movie(self):
        sql_command = "CREATE TABLE IF NOT EXISTS MOVIES (ID SERIAL PRIMARY KEY, movie_title VARCHAR(200), movie_description VARCHAR(400), movie_image VARCHAR(200), movie_rating FLOAT)"
        self.cursor_helper.cursor_execute(sql_command=sql_command)

    def add_movie(self, movie, admin_id):
        sql_command = "INSERT INTO MOVIES (movie_title, movie_description, movie_image, movie_rating) VALUES ( %(movie_title)s, %(movie_description)s, %(movie_image)s, %(movie_rating)s) RETURNING id"
        variables = {'movie_title': movie.movie_title, 'movie_description': movie.movie_description,
                     'movie_image': movie.movie_image, 'movie_rating': movie.movie_rating}
        movie_id = self.cursor_helper.cursor_fetch_one(
            sql_command=sql_command, variables=variables)[0]
        self.add_admin_added(movie_id, admin_id)

    def get_movie(self, movie_id):
        sql_command = "SELECT * FROM MOVIES WHERE(ID = %(id)s)"
        variables = {"id": movie_id}
        result = self.cursor_helper.cursor_fetch_one(
            sql_command=sql_command, variables=variables)
        if len(result) == 0:
            return None
        return Movie(*result)

    def delete_movie(self, movie_id):
        sql_command = "DELETE FROM MOVIES WHERE ( id = %(movie_id)s ) "
        variables = {'movie_id': movie_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def update_movie(self, movie):
        sql_command = "UPDATE MOVIES SET movie_title = %(movie_title)s, movie_description = %(movie_description)s, movie_image = %(movie_image)s  WHERE ( id = %(movie_id)s ) "
        variables = {'movie_title': movie.movie_title, 'movie_description': movie.movie_description,
                     'movie_image': movie.movie_image, 'movie_id': movie.id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def get_all_movies(self):
        sql_command = "SELECT * FROM MOVIES"
        results = self.cursor_helper.cursor_fetch_all(
            sql_command=sql_command)
        return [Movie(*item) for item in results]

    def get_movie_rating_count(self, movie_id):
        sql_command = "SELECT count(*) FROM RATINGS where( movie_id = %(movie_id)s )"
        variables = {'movie_id': movie_id}
        result = self.cursor_helper.cursor_fetch_one(sql_command, variables)
        print(result)
        return result[0]

    def calculate_rating(self, movie_id):
        sql_command = "SELECT SUM(rating) FROM RATINGS WHERE( movie_id =%(movie_id)s)"
        variables = {'movie_id': movie_id}
        result = self.cursor_helper.cursor_fetch_one(sql_command, variables)
        return result[0]

    def update_movie_rating(self, movie_id):
        rating_count = self.get_movie_rating_count(movie_id)
        try:
            new_rating = self.calculate_rating(movie_id) / rating_count
        except:
            new_rating = None
        sql_command = "UPDATE MOVIES SET movie_rating = %(movie_rating)s WHERE (ID = %(movie_id)s)"
        variables = {'movie_rating': new_rating, 'movie_id': movie_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def create_friends(self):
        sql_command = "CREATE TABLE IF NOT EXISTS FRIENDS (USER_ID INT, FRIEND_ID INT,FOREIGN KEY (USER_ID) REFERENCES USERS(ID) ON DELETE CASCADE, FOREIGN KEY (FRIEND_ID) REFERENCES USERS(ID) ON DELETE CASCADE, PRIMARY KEY (USER_ID, FRIEND_ID) )"
        self.cursor_helper.cursor_execute(sql_command=sql_command)

    def add_friend(self, user_id, friend_username):
        friend_id = self.get_user_id(friend_username)
        sql_command = "INSERT INTO FRIENDS (USER_ID,FRIEND_ID) VALUES ( %(user_id)s, %(friend_id)s)"
        variables = {'user_id': user_id, 'friend_id': friend_id}
        self.cursor_helper.cursor_execute(
            sql_command=sql_command, variables=variables)

    def get_all_friends(self, user_id):
        sql_command = "SELECT FRIEND_ID,USERNAME FROM FRIENDS JOIN USERS ON friend_id = id WHERE (user_id = %(user_id)s or friend_id = %(user_id)s)"
        variables = {'user_id': user_id}
        results = self.cursor_helper.cursor_fetch_all(
            sql_command=sql_command, variables=variables)
        return [Friend(*item) for item in results]

    def create_ratings(self):
        sql_command = "CREATE TABLE IF NOT EXISTS RATINGS (USER_ID INT, MOVIE_ID INT, RATING INT,FOREIGN KEY (USER_ID) REFERENCES USERS(ID) ON DELETE CASCADE, FOREIGN KEY (MOVIE_ID) REFERENCES MOVIES(ID) ON DELETE CASCADE, PRIMARY KEY (USER_ID, MOVIE_ID) )"
        self.cursor_helper.cursor_execute(sql_command=sql_command)

    def add_rating(self, rating_obj):
        sql_command = "INSERT INTO RATINGS (user_id, movie_id, rating) VALUES ( %(user_id)s, %(movie_id)s, %(rating)s)"
        variables = {'user_id': rating_obj.user_id,
                     'movie_id': rating_obj.movie_id, 'rating': rating_obj.user_rating}
        self.cursor_helper.cursor_execute(
            sql_command=sql_command, variables=variables)

    def update_rating(self, rating_obj):
        sql_command = "UPDATE RATINGS SET rating = %(new_rating)s WHERE (user_id = %(user_id)s and movie_id =%(movie_id)s)"
        variables = {'user_id': rating_obj.user_id,
                     'movie_id': rating_obj.movie_id, 'new_rating': rating_obj.user_rating}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def delete_rating(self, user_id, movie_id):
        sql_command = "DELETE FROM RATINGS WHERE( user_id = %(user_id)s and movie_id = %(movie_id)s )"
        variables = {'user_id': user_id, 'movie_id': movie_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def get_all_rated_movies(self, user_id):
        sql_command = "SELECT movies.id ,movies.movie_title, ratings.rating FROM RATINGS JOIN MOVIES ON ratings.movie_id = movies.id WHERE (user_id = %(user_id)s)"
        variables = {'user_id': user_id}
        results = self.cursor_helper.cursor_fetch_all(sql_command, variables)
        return [MovieWithRating(*item) for item in results]

    def delete_rating(self, user_id, movie_id):
        sql_command = "DELETE FROM RATINGS WHERE (user_id = %(user_id)s and movie_id = %(movie_id)s )"
        variables = {'user_id': user_id, 'movie_id': movie_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def get_rating(self, user_id, movie_id):
        sql_command = "SELECT * FROM RATINGS WHERE (user_id = %(user_id)s and movie_id = %(movie_id)s)"
        variables = {'user_id': user_id, 'movie_id': movie_id}
        results = self.cursor_helper.cursor_fetch_one(sql_command, variables)
        if results is None:
            return None
        return Rating(*results)

    def create_favorites(self):
        sql_command = "CREATE TABLE IF NOT EXISTS FAVORITES (USER_ID INT, MOVIE_ID INT,FOREIGN KEY (USER_ID) REFERENCES USERS(ID) ON DELETE CASCADE, FOREIGN KEY (MOVIE_ID) REFERENCES MOVIES(ID) ON DELETE CASCADE, PRIMARY KEY (USER_ID, MOVIE_ID) )"
        self.cursor_helper.cursor_execute(sql_command=sql_command)

    def add_favorite(self, user_id, movie_id):
        sql_command = "INSERT INTO FAVORITES (user_id, movie_id) VALUES( %(user_id)s, %(movie_id)s)"
        variables = {'user_id': user_id, 'movie_id': movie_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def is_movie_favorite(self, user_id, movie_id):
        sql_command = "SELECT * FROM FAVORITES WHERE(user_id = %(user_id)s and movie_id = %(movie_id)s)"
        variables = {'user_id': user_id, 'movie_id': movie_id}
        result = self.cursor_helper.cursor_fetch_one(sql_command, variables)
        return result != None

    def get_all_favorite_movies(self, user_id):
        print(user_id)
        sql_command = "SELECT movies.* FROM FAVORITES JOIN MOVIES ON movie_id = id WHERE (user_id = %(user_id)s)"
        variables = {'user_id': user_id}
        results = self.cursor_helper.cursor_fetch_all(sql_command, variables)
        return [Movie(*item) for item in results]

    def delete_favorite(self, user_id, movie_id):
        sql_command = "DELETE FROM FAVORITES WHERE (user_id = %(user_id)s and movie_id = %(movie_id)s )"
        variables = {'user_id': user_id, 'movie_id': movie_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def create_admin(self):
        sql_command = "CREATE TABLE IF NOT EXISTS ADMINS (ID SERIAL PRIMARY KEY, USER_ID INT, FOREIGN KEY (USER_ID) REFERENCES USERS(ID) ON DELETE CASCADE  )"
        self.cursor_helper.cursor_execute(sql_command=sql_command)

    def create_admin_added(self):
        sql_command = "CREATE TABLE IF NOT EXISTS ADMIN_ADDED (ADMIN_ID INT, MOVIE_ID INT,FOREIGN KEY (ADMIN_ID) REFERENCES ADMINS(ID) ON DELETE CASCADE, FOREIGN KEY (MOVIE_ID) REFERENCES MOVIES(ID) ON DELETE CASCADE, PRIMARY KEY (ADMIN_ID, MOVIE_ID) )"
        self.cursor_helper.cursor_execute(sql_command=sql_command)

    def add_admin_added(self, movie_id,  admin_id):
        sql_command = "INSERT INTO ADMIN_ADDED (admin_id, movie_id) VALUES( %(admin_id)s, %(movie_id)s)"
        variables = {'admin_id': admin_id, 'movie_id': movie_id}
        self.cursor_helper.cursor_execute(sql_command, variables)

    def is_user_admin(self, user_id):
        sql_command = "SELECT * FROM ADMINS WHERE( user_id = %(user_id)s)"
        variables = {'user_id': user_id}
        result = self.cursor_helper.cursor_fetch_one(sql_command, variables)
        return result != None

    def get_admin_id(self, user_id):
        sql_command = "SELECT ID FROM ADMINS WHERE( user_id = %(user_id)s)"
        variables = {'user_id': user_id}
        result = self.cursor_helper.cursor_fetch_one(sql_command, variables)
        return result[0]
