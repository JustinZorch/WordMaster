from flask import Blueprint, render_template

from common.database import Database


groups_blueprint = Blueprint('groups', __name__)

@groups_blueprint.route('/', methods=['POST', 'GET'])
def index():
    # return users without words dictionary
    users = Database.all("users", {"words": 0})

    # 0 is for global, maybe in the future indv groups
    # sort users according to total points
    sorted_users = sorted(users, key=lambda d: d["groups"][0]["total_points"], reverse=True)


    return render_template('groups/main.html', users=sorted_users)

