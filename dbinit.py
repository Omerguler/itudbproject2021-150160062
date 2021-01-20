import os
import sys

from database import Database
from models import User

if __name__ == "__main__":

    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    else:
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

    # initialize(url)
