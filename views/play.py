
from datetime import timedelta, datetime, date


from flask import Blueprint, render_template, request, session, flash


from common.database import Database
from models.Check import Check
from models.user.decorators import requires_login

play_blueprint = Blueprint('play', __name__)


def letters_f(req, num):

    """"
        returns the input from the form if POST in a list
    """

    if req == "POST":
        letters = []
        for i in range(1, num + 1):
            temp = "letter" + str(i)
            let = request.form.get(temp)
            letters.append(let.upper())

        return True, letters
    return False, []


def check_f(letters, num):

    """"
        checks the input against the word of the day via the Check class
    """

    check = Check(letters)
    if check.allowed():
        state, points_add = check.correct_word()
        check.check()


        if state:
            now = datetime.now()
            today = now.date()
            today_s = today.strftime("%Y%m%d")
            data = Database.find_one("dicts", {"name": str(num)})
            list_dict = data["random"]
            today_word = list_dict[today_s]
            return True, today_word, points_add
        else:
            return False, '', 0
    else:
        flash('Please enter a valid word', 'danger')
        return False, '', 0


def page_vars(num):

    # get todays date string
    now = datetime.now()
    today = now.date()
    today_s = today.strftime("%Y%m%d")

    #load in users data excluding the words dict
    user_data = Database.find_one_return_one('users', {"email": session['email']}, {f"words.{today_s}": 1})
    alphabet = user_data["words"][today_s][num-3]["dict"]
    guesses = user_data["words"][today_s][num-3]["guesses"]
    state_bool = user_data["words"][today_s][num-3][str(num)]

    # calculate time till new word, maybe can do this in java ???
    today = datetime.combine(date.today(), datetime.min.time())
    tomorrow = today + timedelta(days=1)
    time = (tomorrow - datetime(1970, 1, 1)).total_seconds()

    return alphabet, guesses, state_bool, time


# can we make all these urls a single function?
@play_blueprint.route('/3letters', methods=['POST', 'GET'])
@requires_login
def letters_3():

    points = [30, 20, 15, 10, 5]
    num = 3
    req = request.method

    bool_post, letters = letters_f(req, num)

    if bool_post:
        bool_check, today_word, points_add = check_f(letters, num)

        if bool_check:
            return render_template("play/correct.html", word=today_word, points=points_add)

    alphabet, guesses, state_bool, time = page_vars(num)

    return render_template("play/main.html", alphabet=alphabet, length=num, guesses=guesses, points=points,
                           state_bool=state_bool, time=time)


@play_blueprint.route('/4letters', methods=['POST', 'GET'])
@requires_login
def letters_4():
    points = [30, 20, 15, 10, 5]
    num = 4
    req = request.method

    bool_post, letters = letters_f(req, num)

    if bool_post:
        bool_check, today_word, points_add = check_f(letters, num)

        if bool_check:
            return render_template("play/correct.html", word=today_word, points=points_add)

    alphabet, guesses, state_bool, time = page_vars(num)

    return render_template("play/main.html", alphabet=alphabet, length=num, guesses=guesses, points=points,
                           state_bool=state_bool, time=time)


@play_blueprint.route('/5letters', methods=['POST', 'GET'])
@requires_login
def letters_5():
    points = [30, 20, 15, 10, 5]
    num = 5
    req = request.method

    bool_post, letters = letters_f(req, num)

    if bool_post:
        bool_check, today_word, points_add = check_f(letters, num)

        if bool_check:
            return render_template("play/correct.html", word=today_word, points=points_add)

    alphabet, guesses, state_bool, time = page_vars(num)

    return render_template("play/main.html", alphabet=alphabet, length=num, guesses=guesses, points=points,
                           state_bool=state_bool, time=time)


@play_blueprint.route('/6letters', methods=['POST', 'GET'])
@requires_login
def letters_6():
    points = [40, 30, 20, 15, 10, 5]
    num = 6
    req = request.method

    bool_post, letters = letters_f(req, num)

    if bool_post:
        bool_check, today_word, points_add = check_f(letters, num)

        if bool_check:
            return render_template("play/correct.html", word=today_word, points=points_add)

    alphabet, guesses, state_bool, time = page_vars(num)

    return render_template("play/main.html", alphabet=alphabet, length=num, guesses=guesses, points=points,
                           state_bool=state_bool, time=time)


@play_blueprint.route('/7letters', methods=['POST', 'GET'])
@requires_login
def letters_7():
    points = [40, 30, 20, 15, 10, 5]
    num = 7
    req = request.method

    bool_post, letters = letters_f(req, num)

    if bool_post:
        bool_check, today_word, points_add = check_f(letters, num)

        if bool_check:
            return render_template("play/correct.html", word=today_word, points=points_add)

    alphabet, guesses, state_bool, time = page_vars(num)

    return render_template("play/main.html", alphabet=alphabet, length=num, guesses=guesses, points=points,
                           state_bool=state_bool, time=time)


@play_blueprint.route('/8letters', methods=['POST', 'GET'])
@requires_login
def letters_8():
    points = [40, 30, 20, 15, 10, 5]
    num = 8
    req = request.method

    bool_post, letters = letters_f(req, num)

    if bool_post:
        bool_check, today_word, points_add = check_f(letters, num)

        if bool_check:
            return render_template("play/correct.html", word=today_word, points=points_add)

    alphabet, guesses, state_bool, time = page_vars(num)

    return render_template("play/main.html", alphabet=alphabet, length=num, guesses=guesses, points=points,
                           state_bool=state_bool, time=time)


@play_blueprint.route('/9letters', methods=['POST', 'GET'])
@requires_login
def letters_9():
    points = [40, 30, 20, 15, 10, 5]
    num = 9
    req = request.method

    bool_post, letters = letters_f(req, num)

    if bool_post:
        bool_check, today_word, points_add = check_f(letters, num)

        if bool_check:
            return render_template("play/correct.html", word=today_word, points=points_add)

    alphabet, guesses, state_bool, time = page_vars(num)

    return render_template("play/main.html", alphabet=alphabet, length=num, guesses=guesses, points=points,
                           state_bool=state_bool, time=time)
