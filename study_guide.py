import psycopg2

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
        print "User created successfully:", name
        connection.commit()
    except:
        print "Could not create user - make sure your username is unique"


def add_study_guide_to_db(name, owner_id):
    try:
        cursor.execute("""INSERT INTO study_guides(name, owner_id) VALUES('%s', '%s');
        SELECT currval('study_guides_id_seq');""" % (name, owner_id))
        print "Study guide created successfully:", name
        connection.commit()
    except:
        print "Could not create study guide"

    return cursor.fetchone()[0]


def get_study_guides_for_user(owner_id):
    try:
        cursor.execute("""SELECT id, name FROM study_guides WHERE owner_id = '%s';""" % owner_id)
    except:
        could_not_access_db()

    return cursor.fetchall()


# ******** MENUS ********
def select_or_create_user_menu():
    selection = ""

    while selection != "1" and selection != "2" and selection != "3":
        selection = raw_input("1. Select an existing user\n2. Create a new user\n3. Quit\nEnter an option: ")

        if selection is "1":
            select_user()
        elif selection is "2":
            create_user()
        else:
            quit()


def select_or_create_study_guide(user_id):
    selection = ""

    while selection != "1" and selection != "2":
        selection = raw_input("1. Select exisiting study guide\n2. Create a new study guide\nSelect an option: ")

    if selection is "1":
        select_study_guide(user_id)
    else:
        create_study_guide(user_id)


# ******** USER MANAGEMENT ********
def create_user():
    name = raw_input("Enter name of user: ")
    add_user_to_db(name)
    select_or_create_user_menu()


def select_user():
    selection = "0"
    users = get_users()
    ids = []
    for (id, name) in users:
        print("%s: %s" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a user's number: ")

    select_or_create_study_guide(int(selection))


# ******** STUDY GUIDE MANAGEMENT ********
def select_study_guide(user_id):
    selection = "0"
    study_guides = get_study_guides_for_user(user_id)
    ids = []

    if len(study_guides) == 0:
        print "No study guides for selected user! Please create a study guide."
        select_or_create_study_guide(user_id)

    for (id, name) in study_guides:
        print("%s: %s" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a study guide number: ")

    begin_studying(int(selection))


def create_study_guide(user_id):
    name = raw_input("Enter name of study guide: ").replace("'", "''")
    study_guide_id = add_study_guide_to_db(name, user_id)
    select_or_create_study_guide(user_id)


# ******** STUDYING ********
def begin_studying(study_guide_id):
    return


# ******** MAIN ********
if __name__ == '__main__':
    select_or_create_user_menu()