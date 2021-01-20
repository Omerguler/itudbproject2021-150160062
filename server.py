from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import views
from database import Database
from models import User

lm = LoginManager()
database = Database()


@lm.user_loader
def load_user(user_id):
    return database.get_user(user_id)


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_object("settings")
app.add_url_rule("/signin", view_func=views.sign_in, methods=['GET', 'POST'])
app.add_url_rule("/signup", view_func=views.sign_up, methods=['GET', 'POST'])
app.add_url_rule("/", view_func=views.movies_page, methods=['GET', 'POST'])
app.add_url_rule("/profile", view_func=views.profile, methods=['GET', 'POST'])
app.add_url_rule("/add_friend", view_func=views.add_friend,
                 methods=['GET', 'POST'])
app.add_url_rule("/friends", view_func=views.friends,
                 methods=['GET'])
app.add_url_rule("/user/<username>", view_func=views.user_profile,
                 methods=['GET', 'POST'])
app.add_url_rule("/movie/<movie_id>", view_func=views.movie_details,
                 methods=['GET', 'POST'])
app.add_url_rule("/update_movie/<movie_id>", view_func=views.update_movie,
                 methods=['GET', 'POST'])
app.add_url_rule("/delete_movie/<movie_id>", view_func=views.delete_movie,
                 methods=['GET', 'POST'])
app.add_url_rule("/signout", view_func=views.sign_out, methods=['GET', 'POST'])
app.add_url_rule("/admin_page", view_func=views.admin_page,
                 methods=['GET', 'POST'])

lm.init_app(app)
lm.login_view = "sign_in"

if __name__ == "__main__":
    database = Database()
    database.create_user()
    database.create_admin()
    database.create_admin_added()
    database.create_favorites()
    database.create_friends()
    database.create_movie()
    database.create_ratings()
    database.add_user(User(0, "admin_account", "123456789",
                           "1998-08-06", "admin@gmail.com"))
    database.add_admin(1)
    app.run()
