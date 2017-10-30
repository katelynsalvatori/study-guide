import psycopg2
from random import shuffle

# COLORS!
DEFAULT = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'

# ******** DATABASE ********
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


# ******** MENUS ********
def user_menu():
    print "-----USER MENU-----"
    selection = ""

    choices = [str(x) for x in range(1, 4)]

    while selection not in choices:
        selection = raw_input("1. Select an existing user\n2. Create a new user\n3. Quit\nEnter an option: ")

    if selection is "1":
        select_user()
    elif selection is "2":
        create_user()
    else:
        quit()


def study_guide_menu(user_id):
    print "-----STUDY GUIDE MENU-----"
    selection = ""

    choices = [str(x) for x in range(1, 4)]

    while selection not in choices:
        selection = raw_input(
            "1. Select exisiting study guide\n2. Create a new study guide\n3. Quit\nSelect an option: ")

    if selection is "1":
        select_study_guide(user_id)
    elif selection is "2":
        create_study_guide(user_id)
    else:
        quit()


# ******** USER MANAGEMENT ********
def create_user():
    print "-----USER CREATION-----"
    name = raw_input("Enter name of user: ")
    add_user_to_db(name)
    user_menu()


def select_user():
    print "-----USERS-----"
    selection = "0"
    users = get_users()

    if len(users) == 0:
        print "No users! Please create a user."
        user_menu()

    ids = []
    for (id, name) in users:
        print("%s: %s" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a user's number: ")

    study_guide_menu(int(selection))


# ******** STUDY GUIDE MANAGEMENT ********
def select_study_guide(user_id):
    print "-----STUDY GUIDES----"
    selection = "0"
    study_guides = get_study_guides_for_user(user_id)
    ids = []

    if len(study_guides) == 0:
        print "No study guides for selected user! Please create a study guide."
        study_guide_menu(user_id)

    for (id, name) in study_guides:
        print("%s: %s" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a study guide number: ")

    study(int(selection))


def create_study_guide(user_id):
    print "-----STUDY GUIDE CREATION-----"
    name = raw_input("Enter name of study guide: ").replace("'", "''")
    study_guide_id = add_study_guide_to_db(name, user_id)
    create_questions(study_guide_id)
    study_guide_menu(user_id)


def create_questions(study_guide_id):
    more_questions = True
    index = 1

    while more_questions:
        print "Question %s." % index
        question_text = raw_input("Enter question text: ").replace("'", "''")
        question_id = add_question_to_db(question_text, study_guide_id)
        create_answers(question_id)
        more = ""
        while more != "y" and more != "n":
            more = raw_input("More questions? (y/n): ")
        more_questions = more == "y"
        index += 1


def create_answers(question_id):
    more_answers = True
    index = 1

    while more_answers:
        print "Answer %s." % index
        answer_text = raw_input("Enter answer text: ").replace("'", "''")
        add_answer_to_db(answer_text, question_id)
        more = ""
        while more != "y" and more != "n":
            more = raw_input("More answers? (y/n): ")
        more_answers = more == "y"
        index += 1


# ******** STUDYING ********
def study(study_guide_id):
    questions = get_questions_from_study_guide(study_guide_id)
    shuffle(questions)
    num_correct = 0
    index = 1

    for (question_id, question_text) in questions:
        answers = get_answers_of_question(question_id)
        print BLUE + "---QUESTION %s---" % index + DEFAULT
        print question_text
        print "(Number of answers: %s)" % len(answers)
        correct = process_answers([x.lower() for x in answers])
        num_correct += 1 if correct else 0

        if not correct:
            print_answers(answers)

        index += 1

    percent_correct = 0 if len(questions) == 0 else (float(num_correct) / float(len(questions))) * 100
    print "-----RESULTS-----"
    print "Correct answers: %s / %s = %.2f%%" % (num_correct, len(questions), percent_correct)
    user_menu()


def process_answers(answers):
    entered_answers = set()
    for i in range(0, len(answers)):
        answer = raw_input("Answer %s: " % str(i + 1)).lower()

        if answer in answers and answer not in entered_answers:
            print GREEN + "Correct answer" + DEFAULT
        elif answer not in answers:
            print YELLOW + "Incorrect answer" + DEFAULT
            return False
        elif answer in entered_answers:
            print YELLOW + "You have already entered this answer" + DEFAULT
            return False
        entered_answers.add(answer)
    return True


def print_answers(answers):
    print "ANSWERS:"
    for index in range (0, len(answers)):
        print "%d. %s" % (index + 1, answers[index])


# ******** MAIN ********
if __name__ == '__main__':
    user_menu()