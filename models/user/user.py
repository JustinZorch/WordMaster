import json
from datetime import datetime, timedelta
from typing import Dict

from flask import flash

from common.database import Database
from common.utils import Utils
import models.user.errors as UserErrors
from models import user
from models.Letter import Letter


class User:

    # clean up?

    def __init__(self, email, password, name, words=None,
                 groups=None):

        if words is None:
            words = {}
        if groups is None:
            groups = [{"group_name": "global", "total_points": 0,
                       "points": [{"name": "3", "points": 0, "attempts": 0},
                                  {"name": "4", "points": 0, "attempts": 0},
                                  {"name": "5", "points": 0, "attempts": 0},
                                  {"name": "6", "points": 0, "attempts": 0},
                                  {"name": "7", "points": 0, "attempts": 0},
                                  {"name": "8", "points": 0, "attempts": 0},
                                  {"name": "9", "points": 0, "attempts": 0}]}]

        self.collection = "users"
        self.email = email
        self.password = password
        self.name = name
        self.groups = groups
        self.words = words

    def find_by_email(email: str):

        return Database.find_one("users", {"email": email})

    def register_user(email, password, name):
        new_user = User(email, password, name)
        new_user.create_words()
        Database.insert(new_user.collection, new_user.json())

    def is_email_used(email: str):

        if User.find_by_email(email) is None:
            return True
        else:
            return False

    def json(self) -> Dict:
        return {
            "email": self.email,
            "password": Utils.hash_password(self.password),
            "name": self.name,
            "groups": self.groups,
            "words": self.words
        }

    def is_login_valid(email: str, password: str) -> bool:
        user = Database.find_one("users", {"email": email})
        if user is not None:

            if not Utils.check_hashed_password(password, user["password"]):
                ## raise UserErrors.IncorrectPasswordError('Your password was incorrect.')
                return False
        else:
            flash("No such e-mail is registered.", "danger")
            return False

        return True

    def create_words(self):

        A = {"letter": "", "class": "letter"}
        THREE = [A, A, A]
        FOUR = [A, A, A, A]
        FIVE = [A, A, A, A, A]
        SIX = [A, A, A, A, A, A]
        SEVEN = [A, A, A, A, A, A, A]
        EIGHT = [A, A, A, A, A, A, A, A]
        NINE = [A, A, A, A, A, A, A, A, A]

        data = [{"3": False, "count": 0, "dict": [], "guesses": [THREE, THREE, THREE, THREE, THREE]},
                {"4": False, "count": 0, "dict": [], "guesses": [FOUR, FOUR, FOUR, FOUR, FOUR]},
                {"5": False, "count": 0, "dict": [], "guesses": [FIVE, FIVE, FIVE, FIVE, FIVE]},
                {"6": False, "count": 0, "dict": [], "guesses": [SIX, SIX, SIX, SIX, SIX, SIX]},
                {"7": False, "count": 0, "dict": [], "guesses": [SEVEN, SEVEN, SEVEN, SEVEN, SEVEN, SEVEN]},
                {"8": False, "count": 0, "dict": [], "guesses": [EIGHT, EIGHT, EIGHT, EIGHT, EIGHT, EIGHT]},
                {"9": False, "count": 0, "dict": [], "guesses": [NINE, NINE, NINE, NINE, NINE, NINE]}]

        row1 = []
        row1_letters = "QWERTYUIOP"
        for i in range(10):
            row1.append(Letter(i, row1_letters[i]).json())

        row2 = []
        row2_letters = "ASDFGHJKL"
        for i in range(9):
            row2.append(Letter(i, row2_letters[i]).json())

        row3 = []
        row3_letters = "ZXCVBNM"
        for i in range(7):
            row3.append(Letter(i, row3_letters[i]).json())

        for i in range(7):
            data[i]["dict"].append(row1)
            data[i]["dict"].append(row2)
            data[i]["dict"].append(row3)

        now = datetime.now()
        today = now.date()

        ### creating data space for 100 days
        for j in range(100):
            today_s = today.strftime("%Y%m%d")
            self.words[today_s] = data
            today += timedelta(days=1)

        if self.words == {}:
            self.words = data

