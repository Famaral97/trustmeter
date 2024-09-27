from flask import Blueprint, render_template, request, jsonify
import random

from app.utils import POLITICAL_PARTIES
from app.utils.database import connect, get_member_by_name, with_db_connection

party_bp = Blueprint('party', __name__)

@party_bp.route("/games/guess-party", methods=['GET'])
@with_db_connection
def get_guess_party_game(cursor, db):

    random_member_query = """
    SELECT * FROM members
    ORDER BY RAND()
    LIMIT 1;
    """
    cursor.execute(random_member_query)
    random_member = cursor.fetchone()

    correct_party = random_member["party"]
    other_parties = [party for party in POLITICAL_PARTIES if party != correct_party]
    options = random.sample(other_parties, 3) + [correct_party]
    random.shuffle(options)

    return render_template("guessParty.html", member=random_member, options=options)


@party_bp.route("/games/guess-party/check", methods=['POST'])
@with_db_connection
def check_party_guess(cursor, db):

    data = request.json
    member_name = data.get('member')

    member = get_member_by_name(cursor, member_name)

    return jsonify({'correct_party': member["party"]})
