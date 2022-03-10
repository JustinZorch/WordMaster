from flask import Blueprint, render_template


how_to_play_blueprint = Blueprint('how_to_play', __name__)


@how_to_play_blueprint.route('/how_to_play', methods=['POST', 'GET'])
def index():

    return render_template("howtoplay/how_to_play.html")

