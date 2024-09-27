from flask import Blueprint, render_template, request, jsonify
import random

from app.utils import POLITICAL_PARTIES
from app.utils.database import connect, get_member_by_name, with_db_connection

intruder_bp = Blueprint('intruder', __name__)


@intruder_bp.route('/games/intruder')
@with_db_connection
def intruder_game(cursor, db):
    
    party = random.choice(POLITICAL_PARTIES[:-2]) # pan and cds do not have 3 members

    random_members_from_party_query = """
    SELECT * FROM members
    WHERE party = %s
    ORDER BY RAND()
    LIMIT 3;
    """
    cursor.execute(random_members_from_party_query, (party,))
    random_members_from_party = cursor.fetchall()

    random_member_query = """
    SELECT * FROM members
    WHERE party <> %s
    ORDER BY RAND()
    LIMIT 1;
    """
    cursor.execute(random_member_query, (party,))
    random_member = cursor.fetchone()

    options = random_members_from_party + [random_member]
    random.shuffle(options)

    return render_template('intruder.html', members=options)


@intruder_bp.route('/games/intruder/check', methods=['POST'])
@with_db_connection
def check_intruder(cursor, db):

    data = request.get_json()
    members_names = data['members']
    members = [get_member_by_name(cursor, member_name) for member_name in members_names]
    selected_name = data['selected_name']

    parties = [member['party'] for member in members]
    majority_party = max(set(parties), key=parties.count)

    intruder = next(member for member in members if member['party'] != majority_party)
    intruder_name = intruder['name']

    is_intruder = selected_name == intruder_name

    return jsonify({
        'is_intruder': is_intruder,
        'intruder_name': intruder_name,
        'selected_name': selected_name,
        "majority_party": majority_party,
        "intruder_party": intruder['party']
    })
