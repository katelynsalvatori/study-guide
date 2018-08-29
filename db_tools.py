import psycopg2

try:
    connection = psycopg2.connect("dbname='study_guide' user='admin' host='localhost' password=''")
except:
    print "ERROR: Unable to connect to the database"
    quit()

cursor = connection.cursor()


def could_not_access_db():
    print "Could not access the database"
    quit()


def get_users():
    try:
        cursor.execute("""SELECT * FROM users;""")
    except:
        could_not_access_db()

    return cursor.fetchall()


def add_user_to_db(name):
    try:
        cursor.execute("""INSERT INTO users(name) VALUES('%s');""" % name)
        print "User created successfully"
        connection.commit()
    except:
        print "Could not create user - make sure your username is unique"

def delete_user_from_db(user_id):
    try:
        cursor.execute("""DELETE FROM users WHERE id = %s;""" % user_id)
        print "User deleted successfully"
        connection.commit()
    except:
        print "Could not delete user"

def update_user_name_in_db(user_id, new_name):
    try:
        cursor.execute("""UPDATE users SET name = '%s' WHERE id = %s""" % (new_name, user_id))
        print "User name updated successfully"
        connection.commit()
    except:
        print "Could not update username - make sure your new name is unique"


def add_study_guide_to_db(name, owner_id):
    try:
        cursor.execute("""INSERT INTO study_guides(name, owner_id) VALUES('%s', '%s');
        SELECT currval('study_guides_id_seq');""" % (name, owner_id))
        print "Study guide created successfully"
        connection.commit()
    except:
        print "Could not create study guide"

    return cursor.fetchone()[0]


def add_question_to_db(question_text, study_guide_id):
    try:
        cursor.execute("""INSERT INTO questions(question_text, study_guide_id) VALUES('%s', '%s');
        SELECT currval('questions_id_seq');""" % (question_text, study_guide_id))
        print "Question created successfully"
        connection.commit()
    except:
        print "Could not create question"

    return cursor.fetchone()[0]


def add_answer_to_db(answer_text, question_id):
    try:
        cursor.execute(
            """INSERT INTO answers(answer_text, question_id) VALUES('%s', '%s');""" % (answer_text, question_id))
        print "Answer created successfully"
        connection.commit()
    except:
        print "Could not create answer"


def get_study_guides_for_user(owner_id):
    try:
        cursor.execute("""SELECT id, name FROM study_guides WHERE owner_id = '%s';""" % owner_id)
    except:
        could_not_access_db()

    return cursor.fetchall()


def get_questions_from_study_guide(study_guide_id):
    try:
        cursor.execute("""SELECT id, question_text FROM questions WHERE study_guide_id = '%s' and enabled;""" % study_guide_id)
    except:
        could_not_access_db()

    return cursor.fetchall()


def get_answers_of_question(question_id):
    try:
        cursor.execute("""SELECT answer_text FROM answers WHERE question_id = '%s';""" % question_id)
    except:
        could_not_access_db()

    return [x[0] for x in cursor.fetchall()]
