from flask import Flask, jsonify, render_template, request

from connect import connect
from elo import calculate_elo

app = Flask(__name__)

db = connect()
cursor = db.cursor(dictionary=True)

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

        print(winner_data, loser_data)

        new_winner_elo, new_loser_elo = calculate_elo(int(winner_data["elo"]), int(loser_data["elo"]))

        print(new_winner_elo, new_loser_elo)

        update_member_elo(db, cursor, winner_data["id"], new_winner_elo)
        update_member_elo(db, cursor, loser_data["id"], new_loser_elo)

        cursor.close()
        db.close()
        return jsonify({"message": f"You chose {winner}"})

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


if __name__ == '__main__':
    app.run()
