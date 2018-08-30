from random import shuffle
import db_tools

# COLORS!
DEFAULT = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'

# ******** MENUS ********
def menu(choice_texts, menu_header = "MENU"):
    print_header(menu_header)

    selection = ""
    choices = [str(x) for x in range(1, len(choice_texts) + 1)]

    for i in range(len(choice_texts)):
        print str(i + 1) + ".", choice_texts[i]

    while selection not in choices:
        selection = raw_input("Enter an option: ")

    return selection

def user_menu():
    choice_texts = [
        "Select an existing user",
        "Create a new user",
        "Delete a user",
        "Update a user's name",
        "Quit"
    ]

    selection = menu(choice_texts, "USER MENU")

    if selection is "1":
        select_user()
    elif selection is "2":
        create_user()
    elif selection is "3":
        delete_user()
    elif selection is "4":
        update_user_name()
    else:
        quit()


def study_guide_menu(user_id):
    choice_texts = [
        "Study an existing study guide",
        "Create a new study guide",
        "Edit a study guide (IN PROGRESS)",
        "Go back",
        "Quit"
    ]
    selection = menu(choice_texts, "STUDY GUIDE MENU")

    if selection is "1":
        study_study_guide(user_id)
    elif selection is "2":
        create_study_guide(user_id)
    elif selection is "3":
        choose_study_guide_to_edit(user_id)
    elif selection is "4":
        user_menu()
    else:
        quit()

def question_edit_menu(question_id, study_guide_id, user_id):
    choice_texts = [
        "Edit question text",
        "Edit answer(s)",
        "Add answer(s)",
        "Delete question",
        "Go back",
        "Quit"
    ]
    selection = menu(choice_texts, "EDIT QUESTION MENU")

    if selection is "1":
        edit_question_text(question_id, study_guide_id, user_id)
    elif selection is "2":
        select_answer_to_edit(question_id, study_guide_id, user_id)
    elif selection is "3":
        create_answers(question_id)
    elif selection is "4":
        delete_question(question_id, study_guide_id, user_id)
    elif selection is "5":
        study_guide_edit_menu(study_guide_id, user_id)
    else:
        quit()

def answer_edit_menu(answer_id, question_id, study_guide_id, user_id):
    choice_texts = [
        "Edit answer text",
        "Delete answer",
        "Go back",
        "Quit"
    ]
    selection = menu(choice_texts, "EDIT ANSWER MENU")

    if selection is "1":
        edit_answer_text(answer_id, question_id, study_guide_id, user_id)
    elif selection is "2":
        delete_answer(answer_id, question_id, study_guide_id, user_id)
    elif selection is "3":
        question_edit_menu(question_id, study_guide_id, user_id)
    else:
        quit()

def study_guide_edit_menu(study_guide_id, user_id):
    choice_texts = [
        "Edit questions/answers",
        "Add question(s)",
        "Delete study guide",
        "Go back",
        "Quit"
    ]
    selection = menu(choice_texts, "EDIT STUDY GUIDE MENU")

    if selection is "1":
        edit_questions(study_guide_id, user_id)
    elif selection is "2":
        create_questions(study_guide_id)
    elif selection is "3":
        delete_study_guide(study_guide_id, user_id)
    elif selection is "4":
        study_guide_menu(user_id)
    else:
        quit()

# ******** USER MANAGEMENT ********
def create_user():
    print_header("USER CREATION")
    name = raw_input("Enter name of user: ")
    db_tools.add_user_to_db(name)
    user_menu()


def select_user():
    print_header("USERS")
    selection = "0"
    users = db_tools.get_users()

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

def delete_user():
    print_header("DELETE USER")
    selection = "0"
    users = db_tools.get_users()

    if len(users) == 0:
        print "No users! Please create a user."
        user_menu()

    ids = []
    for (id, name) in users:
        print("%s: %s" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a user's number to delete: ")

    db_tools.delete_user_from_db(selection)

    user_menu()

def update_user_name():
    print_header("UPDATE USER NAME")
    selection = "0"
    users = db_tools.get_users()

    if len(users) == 0:
        print "No users! Please create a user."
        user_menu()

    ids = []
    for (id, name) in users:
        print("%s: %s" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a user's number to update name: ")

    new_name = raw_input("Enter a new name for the user: ")

    db_tools.update_user_name_in_db(selection, new_name)

    user_menu()


# ******** STUDY GUIDE MANAGEMENT ********
def study_study_guide(user_id):
    study_guide = select_study_guide(user_id)
    study(study_guide)

def select_study_guide(user_id):
    print_header("STUDY GUIDES")
    selection = "0"
    study_guides = db_tools.get_study_guides_for_user(user_id)
    ids = []

    if len(study_guides) == 0:
        print "No study guides for selected user! Please create a study guide."
        study_guide_menu(user_id)

    for (id, name) in study_guides:
        print("%s: %s" % (id, name))
        ids.append(id)

    while int(selection) not in ids:
        selection = raw_input("Enter a study guide number: ")

    return int(selection)


def create_study_guide(user_id):
    print_header("STUDY GUIDE CREATION")
    name = raw_input("Enter name of study guide: ").replace("'", "''")
    study_guide_id = db_tools.add_study_guide_to_db(name, user_id)
    create_questions(study_guide_id)
    study_guide_menu(user_id)


def choose_study_guide_to_edit(user_id):
    study_guide = select_study_guide(user_id)
    study_guide_edit_menu(study_guide, user_id)
    study_guide_menu(user_id)


def edit_questions(study_guide_id, user_id):
    questions = db_tools.get_questions_from_study_guide(study_guide_id)
    ids = []
    print_header("QUESTIONS")

    for (question_id, question_text) in questions:
        print "%d. %s" % (question_id, question_text)
        ids.append(question_id)

    if len(ids) == 0:
        print "No questions to edit! Please add questions first."
        study_guide_edit_menu(study_guide_id, user_id)

    question_selection = 0
    while question_selection not in ids:
        question_selection = int(raw_input("Enter ID of question to edit: "))
    question_edit_menu(question_selection, study_guide_id, user_id)


def create_questions(study_guide_id):
    more_questions = True
    index = 1

    while more_questions:
        print BLUE + "Question %s." % index + DEFAULT
        question_text = raw_input("Enter question text: ").replace("'", "''")
        question_id = db_tools.add_question_to_db(question_text, study_guide_id)
        create_answers(question_id)
        more = ""
        while more != "y" and more != "n":
            more = raw_input(YELLOW + "More questions? (y/n): " + DEFAULT)
        more_questions = more == "y"
        index += 1


def create_answers(question_id):
    more_answers = True
    index = 1

    while more_answers:
        print BLUE + "Answer %s." % index + DEFAULT
        answer_text = raw_input("Enter answer text: ").replace("'", "''")
        db_tools.add_answer_to_db(answer_text, question_id)
        more = ""
        while more != "y" and more != "n":
            more = raw_input(YELLOW + "More answers? (y/n): " + DEFAULT)
        more_answers = more == "y"
        index += 1

def select_answer_to_edit(question_id, study_guide_id, user_id):
    answers = db_tools.get_answers_and_ids_of_questions(question_id)
    ids = []
    print_header("ANSWERS")

    for (answer_id, answer_text) in answers:
        print "%d. %s" % (answer_id, answer_text)
        ids.append(answer_id)

    if len(ids) == 0:
        print "No answers to edit! Please add answers first."
        question_edit_menu(question_id, study_guide_id, user_id)

    answer_selection = 0
    while answer_selection not in ids:
        answer_selection = int(raw_input("Enter ID of answer to edit: "))
    answer_edit_menu(answer_selection, question_id, study_guide_id, user_id)

def edit_question_text(question_id, study_guide_id, user_id):
    new_question_text = raw_input("Enter new question text: ").replace("'", "''")
    db_tools.update_question_text_in_db(question_id, new_question_text)
    question_edit_menu(question_id, study_guide_id, user_id)

def delete_question(question_id, study_guide_id, user_id):
    db_tools.delete_question_from_db(question_id)
    study_guide_edit_menu(study_guide_id, user_id)

def delete_study_guide(study_guide_id, user_id):
    db_tools.delete_study_guide_from_db(study_guide_id)
    study_guide_menu(user_id)

def edit_answer_text(answer_id, question_id, study_guide_id, user_id):
    new_answer_text = raw_input("Enter new answer text: ").replace("'", "''")
    db_tools.update_answer_text_in_db(answer_id, new_answer_text)
    answer_edit_menu(answer_id, question_id, study_guide_id, user_id)

def delete_answer(answer_id, question_id, study_guide_id, user_id):
    db_tools.delete_answer_from_db(answer_id)
    question_edit_menu(question_id, study_guide_id, user_id)


# ******** STUDYING ********
def study(study_guide_id):
    questions = db_tools.get_questions_from_study_guide(study_guide_id)
    shuffle(questions)
    num_correct = 0
    index = 1

    for (question_id, question_text) in questions:
        answers = db_tools.get_answers_of_question(question_id)
        print BLUE + "---QUESTION %s---" % index + DEFAULT
        print question_text
        print "(Number of answers: %s)" % len(answers)
        correct = process_answers([x.lower() for x in answers])
        num_correct += 1 if correct else 0

        if not correct:
            print_answers(answers)

        index += 1

    percent_correct = 0 if len(questions) == 0 else (float(num_correct) / float(len(questions))) * 100
    print_header("RESULTS")
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

def print_header(header):
    print "\n" + BLUE + "-----" + header + "-----" + DEFAULT

# ******** MAIN ********
if __name__ == '__main__':
    try:
        user_menu()
    except SystemExit:
        raise
    except Exception:
        print YELLOW + "Whoops! An error has occurred. Exiting." + DEFAULT
        quit()
