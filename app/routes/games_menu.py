from flask import Blueprint, render_template

games_menu_bp = Blueprint('games_menu', __name__)

@games_menu_bp.route('/games')
def games_menu():
    return render_template("gamesMenu.html")