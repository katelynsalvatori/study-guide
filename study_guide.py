import psycopg2

# ******** DATABASE ********
try:
    connection = psycopg2.connect("dbname='study_guide' user='admin' host='localhost' password=''")
except:
    print "ERROR: Unable to connect to the database"
    quit()

cursor = connection.cursor()

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
        selection = raw_input("1. Select exisiting study guide\n2. Create a new study guide\nSelect an option:")

    if selection is "1":
        select_study_guide(user_id)
    else:
        create_study_guide(user_id)


# ******** USER MANAGEMENT ********
def get_users():
    try:
        cursor.execute("""SELECT * FROM users;""")
    except:
        print "Could not access the database"
        quit()

    return cursor.fetchall()


def create_user():
    name = raw_input("Enter name of user: ")
    try:
        cursor.execute("""INSERT INTO users(name) VALUES('%s');""" % name)
        print "User created successfully:", name
        connection.commit()
    except:
        print "Could not create user - make sure your username is unique"

    select_or_create_user_menu()


def select_user():
    selection = "0"
    users = get_users()
    ids = []
    for (id, name) in users:
        print("""%s: %s""" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a user's number: ")

    select_or_create_study_guide(int(selection))


# ******** STUDY GUIDE MANAGEMENT ********
def select_study_guide(user_id):
    return


def create_study_guide(user_id):
    return

# ******** MAIN ********
if __name__ == '__main__':
    select_or_create_user_menu()