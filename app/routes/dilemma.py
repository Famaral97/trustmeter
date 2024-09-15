from flask import Blueprint, render_template, request, jsonify

from app.utils.database import connect, get_member_by_name, get_member_rank, update_member_elo
from app.utils.elo import calculate_elo

dilemma_bp = Blueprint('dilemma', __name__)


@dilemma_bp.route("/dilemma", methods=['GET', 'POST'])
def get_member_dilemma():
    db = connect()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        data = request.get_json()
        winner = data.get('winner')
        loser = data.get('loser')
        print(f"Person chosen: {winner} (against {loser})")


        winner_data = get_member_by_name(cursor, winner)
        loser_data = get_member_by_name(cursor, loser)

        previous_rank = get_member_rank(cursor, winner)

        new_winner_elo, new_loser_elo = calculate_elo(int(winner_data["elo"]), int(loser_data["elo"]))

        update_member_elo(db, cursor, winner_data["id"], new_winner_elo)
        update_member_elo(db, cursor, loser_data["id"], new_loser_elo)

        new_rank = get_member_rank(cursor, winner)

        cursor.close()
        db.close()
        return jsonify({
            "winner": winner,
            "elo_increase": previous_rank - new_rank
        })

    random_members_query = """
    SELECT * FROM members
    ORDER BY RAND()
    LIMIT 2;
    """

    cursor.execute(random_members_query)
    random_members = cursor.fetchall()
    for member in random_members:
        member.pop("party")

    db.commit()
    cursor.close()
    db.close()
    return render_template("dilemma.html", person1=random_members[0], person2=random_members[1])

@dilemma_bp.route("/dilemma/leaderboard")
def make_leaderboard():
    db = connect()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM members ORDER BY elo DESC;"
    cursor.execute(query)
    members = cursor.fetchall()

    for member in members:
        member.pop("elo")

    db.commit()
    cursor.close()
    db.close()
    return render_template("leaderboard.html", people=members)
