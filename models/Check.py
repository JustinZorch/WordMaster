from copy import deepcopy
from datetime import datetime, time
import time

from flask import session

from common.database import Database


class Check:

    def __init__(self, letters):

        self.cur_letters = letters
        self.org_letters = deepcopy(letters)
        self.length = len(letters)
        self.random_word = None
        self.temp = None
        self.date = ''
        ### do we need self.data
        self.data = None
        self.filter = {"email": session.get('email')}
        self.accept_words = {}

        # good/bad?
        Check.read_date(self)
        Check.read_random(self)
        Check.read_in_data(self)
        Check.read_in_all_words(self)

    def read_random(self):
        # sets the random word
        data = Database.find_one("dicts", {"name": str(self.length)})
        list_dict = data["random"]
        today_word = list(list_dict[self.date])
        self.random_word = deepcopy(today_word)
        self.temp = today_word

    def read_in_all_words(self):
        # read in all acceptable words to a dict
        data = Database.find_one("dicts", {"name": str(self.length)})
        self.accept_words = data["dict"]

    def read_in_data(self):
        # read in all user data to dict
        user_data = Database.find_one("users", self.filter)
        self.data = user_data

    def read_date(self):
        # get todays data as a lookup string
        now = datetime.now()
        today = now.date()
        self.date = today.strftime("%Y%m%d")

    def return_count(self) -> int:
        # finds and returns only relevant info for "count" value
        # not sure if this really does speed up that much
        index = self.length - 3
        filters = {"email": session.get('email')}
        projection = {
            f'words.{self.date}': {
                '$arrayElemAt': [
                    {'$map': {'input': f'$words.{self.date}', 'in': {'count': '$$this.count'}}},
                    index
                ]
            }
        }

        counts = Database.find_one_return_one("users", filters, projection)
        return counts["words"][self.date]["count"]

    def allowed(self):
        # check it word is in allowable dictionary of words
        if "".join(self.org_letters).lower() in self.accept_words:
            return True
        return False

    def points(self):
        # returns the different points setups based on word length
        # 3,4,5 letter words have 5 guesses
        # 6,7,8,9 letter words have 6 guesses

        if self.length < 6:
            return [30, 20, 15, 10, 5]

        if self.length >= 6:
            return [40, 30, 20, 15, 10, 5]

    def correct_word(self):
        # Check if words is 100% correct

        # assume the words is true
        state = True

        # checking words are exact
        for i in range(self.length):
            if self.org_letters[i] != self.random_word[i]:
                state = False
                break

        # if words are 100% exact
        if state:
            print("100% correct function")
            print(self.points())
            print(self.return_count())
            points = self.points()[self.return_count()]
            print(points)

            # updates points, attempts, total points and sets state to True
            # don't think I need to set count to 0
            Database.real_update("users", self.filter, {
                "$inc": {f'groups.0.points.{self.length - 3}.points': points,
                         f'groups.0.points.{self.length - 3}.attempts': 1,
                         f'groups.0.total_points': points},
                "$set": {f'words.{self.date}.{self.length - 3}.{self.length}': True}
            })

            # updating the current in class user data
            self.data["groups"][0]["points"][self.length - 3]["points"] += points
            self.data["groups"][0]["points"][self.length - 3]["attempts"] += 1
            self.data["groups"][0]["total_points"] += points
            self.data["words"][self.date][self.length - 3][str(self.length)] = True
            return True, points
        return False, 0

    def check(self):
        '''
            Check function: takes in the users guess and compares each letter to the random word.
            Assigns different CSS style classes to the letters based on their correctness.
            Does the same to the alphabet and updates.

            Reads the whole user data and essentially inserts it back in.
            Does not use the "quicker, less memory" real_update function
            ### maybe should change this to use it ###
        '''

        # add the letters
        for i in range(self.length):
            self.data["words"][self.date][self.length - 3]["guesses"][self.return_count()][i]["letter"] = \
                self.cur_letters[i]

        # check exact correct letter and correct position
        for i in range(self.length):
            if self.cur_letters[i] == self.random_word[i]:
                self.temp[i] = "!"
                self.cur_letters[i] = "!"
                self.data["words"][self.date][self.length - 3]["guesses"][self.return_count()][i][
                    "class"] = "letter-correct"

        # check correct letter and wrong position
        for i in range(self.length):
            if self.cur_letters[i] != "!":
                for j in range(self.length):
                    if self.cur_letters[i] == self.temp[j]:
                        self.temp[j] = "?"
                        self.cur_letters[i] = "?"
                        self.data["words"][self.date][self.length - 3]["guesses"][self.return_count()][i][
                            "class"] = "letter-maybe"
                        break

        # add the used letter class
        for i in range(self.length):
            if self.cur_letters[i] not in ["!", "?"]:
                self.data["words"][self.date][self.length - 3]["guesses"][self.return_count()][i][
                    "class"] = "letter-used"

        # Create keyboard alphabet setup
        row1_s = "QWERTYUIOP"
        row2_s = "ASDFGHJKL"
        row3_s = "ZXCVBNM"

        # changing the class of alphabet letters used
        for i in range(self.length):

            if self.org_letters[i] in row1_s:
                pos = row1_s.find(self.org_letters[i])
                self.data["words"][self.date][self.length - 3]["dict"][0][pos]["class"] = \
                    self.data["words"][self.date][self.length - 3]["guesses"][self.return_count()][i]["class"]

            elif self.org_letters[i] in row2_s:
                pos = row2_s.find(self.org_letters[i])
                self.data["words"][self.date][self.length - 3]["dict"][1][pos]["class"] = \
                    self.data["words"][self.date][self.length - 3]["guesses"][self.return_count()][i]["class"]

            elif self.org_letters[i] in row3_s:
                pos = row3_s.find(self.org_letters[i])
                self.data["words"][self.date][self.length - 3]["dict"][2][pos]["class"] = \
                    self.data["words"][self.date][self.length - 3]["guesses"][self.return_count()][i]["class"]

        # set guess number and add 1 (count value started at 0 but word length starts from 1)
        # better to store the guess value in the collection
        guess_number = self.return_count() + 1
        allowed_guesses = len(self.data["words"][self.date][self.length - 3]["guesses"])
        correct_word_bool = self.data["words"][self.date][self.length - 3][str(self.length)]

        # user run out of guesses
        # attempt only updated if correct or run out of guesses
        # the word is not incorrect on the last guess
        if (guess_number == allowed_guesses) and (correct_word_bool == False):
            self.data["words"][self.date][self.length - 3][str(self.length)] = True
            self.data["groups"][0]["points"][self.length - 3]["attempts"] += 1

        self.data["words"][self.date][self.length - 3]["count"] = guess_number

        Database.update("users", {"email": session.get('email')}, data=self.data)
