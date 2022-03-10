import os
import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from common.database import Database
from models.user.user import User
from views.groups import groups_blueprint
from views.how_to_play import how_to_play_blueprint
from views.play import play_blueprint
from views.users import user_blueprint


def create_app():

    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config.update(ADMIN=os.environ.get('ADMIN'))


    @app.before_first_request
    def init_db():
        Database.initialize()

    @app.route("/", methods=["GET", "POST"])
    def home():
        return render_template("home.html")


    app.register_blueprint(play_blueprint, url_prefix="/play")
    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(groups_blueprint, url_prefix="/groups")
    app.register_blueprint(how_to_play_blueprint, url_prefix="/how_to_play")

    if __name__ == '__main__':
        app.run(debug=True)

    return app

