from flask import Flask, jsonify, render_template, request
import random

from connect import connect
from elo import calculate_elo

app = Flask(__name__)

db = connect()
cursor = db.cursor(dictionary=True)

POLITICAL_PARTIES = ["PSD", "PS", "CH", "BE", "PCP", "IL", "L", "CDS-PP", "PAN"]

def get_member_rank(cursor, name):
    query = "SELECT * FROM members ORDER BY elo DESC;"
    cursor.execute(query)
    members = cursor.fetchall()

    for i, member in enumerate(members):
        if member["name"] == name:
            return i + 1

def get_member_by_name(cursor, name):
    query = "SELECT * FROM members WHERE name = %s;"
    cursor.execute(query, (name,))
    return cursor.fetchone()

def update_member_elo(db, cursor, member_id, new_elo):
    update_query = "UPDATE members SET elo = %s WHERE id = %s;"
    cursor.execute(update_query, (new_elo, member_id))
    db.commit()

@app.route("/", methods=['GET', 'POST'])
def home():
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
    return render_template("main.html", person1=random_members[0], person2=random_members[1])

@app.route("/leaderboard")
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


@app.route("/guess-party", methods=['GET'])
def get_guess_party_game():
    db = connect()
    cursor = db.cursor(dictionary=True)

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

    db.commit()
    cursor.close()
    db.close()

    return render_template("guessParty.html", member=random_member, options=options)


@app.route("/guess-party/check", methods=['POST'])
def check_party_guess():
    db = connect()
    cursor = db.cursor(dictionary=True)

    data = request.json
    member_name = data.get('member')

    member = get_member_by_name(cursor, member_name)

    db.commit()
    cursor.close()
    db.close()

    return jsonify({'correct_party': member["party"]})


if __name__ == '__main__':
    app.run()
