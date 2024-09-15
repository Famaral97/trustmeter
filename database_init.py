import json

def create_tables(db):
    cursor = db.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS members (
        id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        picture VARCHAR(255),
        circle VARCHAR(100),
        party VARCHAR(50),
        elo INT DEFAULT 1000
    );
    """
    cursor.execute(create_table_query)
    db.commit()

    insert_member_query = """
    INSERT INTO members (id, name, picture, circle, party, elo) 
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    with open("/Users/user/Downloads/members_basic_info.json", "r") as basic_info:
        members_data = json.load(basic_info)

    for member_data in members_data:
        cursor.execute(insert_member_query, (member_data['id'], member_data['name'], member_data['picture'],
                                        member_data['circle'], member_data['party'], 1000))

    db.commit()

    cursor.close()
    db.close()