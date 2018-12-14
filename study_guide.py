from random import shuffle
from difflib import SequenceMatcher
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
        "Edit a study guide",
        "Print a study guide",
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
        choose_study_guide_to_print(user_id)
    elif selection is "5":
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
    question_text = db_tools.get_question_text(question_id)
    selection = menu(choice_texts, "EDIT QUESTION MENU: %s" % question_text)

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
        "Update study guide's name",
        "Go back",
        "Quit"
    ]
    study_guide_name = db_tools.get_study_guide_name(study_guide_id)
    selection = menu(choice_texts, "EDIT STUDY GUIDE MENU: %s" % study_guide_name)

    if selection is "1":
        edit_questions(study_guide_id, user_id)
    elif selection is "2":
        create_questions(study_guide_id)
    elif selection is "3":
        delete_study_guide(study_guide_id, user_id)
    elif selection is "4":
        update_study_guide_name(study_guide_id, user_id)
    elif selection is "5":
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
    for (user_id, name) in users:
        print("%s: %s" % (user_id, name))
        ids.append(str(user_id))

    while selection not in ids:
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
    for (user_id, name) in users:
        print("%s: %s" % (user_id, name))
        ids.append(str(user_id))

    while selection not in ids:
        selection = raw_input("Enter a user's number to delete: ")

    db_tools.delete_user_from_db(int(selection))

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
    study(study_guide, user_id)

def select_study_guide(user_id):
    print_header("STUDY GUIDES")
    selection = "0"
    study_guides = db_tools.get_study_guides_for_user(user_id)
    ids = []

    if len(study_guides) == 0:
        print "No study guides for selected user! Please create a study guide."
        study_guide_menu(user_id)

    for (guide_id, name) in study_guides:
        print("%s: %s" % (guide_id, name))
        ids.append(str(guide_id))

    while selection not in ids:
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

def choose_study_guide_to_print(user_id):
    study_guide = select_study_guide(user_id)
    write_to_txt(study_guide)
    study_guide_menu(user_id)

def edit_questions(study_guide_id, user_id):
    questions = db_tools.get_questions_from_study_guide(study_guide_id)
    ids = []
    print_header("QUESTIONS")

    for (question_id, question_text) in questions:
        print "%s%d.%s %s" % (GREEN, question_id, DEFAULT, question_text)
        ids.append(str(question_id))

    if len(ids) == 0:
        print "No questions to edit! Please add questions first."
        study_guide_edit_menu(study_guide_id, user_id)
    else:
        question_selection = ""
        while question_selection not in ids:
            question_selection = raw_input("%sEnter ID of question to edit: %s" % (GREEN, DEFAULT))
        question_edit_menu(int(question_selection), study_guide_id, user_id)


def create_questions(study_guide_id):
    more_questions = True
    index = 1

    while more_questions:
        print BLUE + "Question %s." % index + DEFAULT
        question_text = raw_input("Enter question text: ").replace("'", "''")
        question_id = db_tools.add_question_to_db(question_text, study_guide_id)
        create_answers(question_id)
        more = ""
        while more not in ["y","n"]:
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
        while more not in ["y","n"]:
            more = raw_input(YELLOW + "More answers? (y/n): " + DEFAULT)
        more_answers = more == "y"
        index += 1

def select_answer_to_edit(question_id, study_guide_id, user_id):
    answers = db_tools.get_answers_and_ids_of_questions(question_id)
    ids = []
    print_header("ANSWERS")

    for (answer_id, answer_text) in answers:
        print "%d. %s" % (answer_id, answer_text)
        ids.append(str(answer_id))

    if len(ids) == 0:
        print "No answers to edit! Please add answers first."
        question_edit_menu(question_id, study_guide_id, user_id)
    else:
        answer_selection = ""
        while answer_selection not in ids:
            answer_selection = raw_input("Enter ID of answer to edit: ")
        answer_edit_menu(int(answer_selection), question_id, study_guide_id, user_id)

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

def update_study_guide_name(study_guide_id, user_id):
    new_name = raw_input("Enter new study guide name: ").replace("'", "''")
    db_tools.update_study_guide_name_in_db(study_guide_id, new_name)
    study_guide_edit_menu(study_guide_id, user_id)

def edit_answer_text(answer_id, question_id, study_guide_id, user_id):
    new_answer_text = raw_input("Enter new answer text: ").replace("'", "''")
    db_tools.update_answer_text_in_db(answer_id, new_answer_text)
    answer_edit_menu(answer_id, question_id, study_guide_id, user_id)

def delete_answer(answer_id, question_id, study_guide_id, user_id):
    db_tools.delete_answer_from_db(answer_id)
    question_edit_menu(question_id, study_guide_id, user_id)


# ******** STUDYING ********
def study(study_guide_id, user_id):
    questions = db_tools.get_questions_from_study_guide(study_guide_id)
    shuffle(questions)
    num_correct = 0
    index = 1

    for (question_id, question_text) in questions:
        answers = db_tools.get_answers_of_question(question_id)
        print BLUE + "---QUESTION %s---" % index + DEFAULT
        print question_text
        print "(Number of answers: %s)" % len(answers)
        correct = process_answers([x.lower().replace("-", " ") for x in answers])
        num_correct += 1 if correct else 0

        if not correct:
            print_answers(answers)

        index += 1

    percent_correct = 0 if len(questions) == 0 else (float(num_correct) / float(len(questions))) * 100
    print_header("RESULTS")
    print "Correct answers: %s / %s = %.2f%%" % (num_correct, len(questions), percent_correct)
    study_guide_menu(user_id)

def tokens_match(str1, str2):
    str1_tokens = str1.split(" ")
    str2_tokens = str2.split(" ")

    if len(str1_tokens) != len(str2_tokens): return False

    for str1_token in str1_tokens:
        if str1_token not in str2_tokens: return False

    for str2_token in str2_tokens:
        if str2_token not in str1_tokens: return False

    return True

def similar_to(answer, possible_answers):
    most_similar = None
    most_similar_ratio = 0.0

    for possible_answer in possible_answers:

        if tokens_match(answer, possible_answer): return (possible_answer, 1.0)

        ratio = SequenceMatcher(None, answer, possible_answer).ratio()
        if ratio > most_similar_ratio:
            most_similar = possible_answer
            most_similar_ratio = ratio

    return (most_similar, most_similar_ratio)

def process_answers(answers):
    entered_answers = set()
    for i in range(0, len(answers)):
        answer = raw_input("Answer %s: " % str(i + 1)).lower().replace("-", " ")

        if answer in answers and answer not in entered_answers:
            print GREEN + "Correct answer" + DEFAULT
            answers.remove(answer)
            entered_answers.add(answer)
        else:
            similarity = similar_to(answer, answers)
            if similarity[1] > 0.5 and similarity[0] not in entered_answers:
                print GREEN + "Partial match" + DEFAULT + "\nCorrect answer: " + similarity[0]
                answers.remove(similarity[0])
                entered_answers.add(similarity[0])
            elif answer not in answers:
                print YELLOW + "Incorrect answer" + DEFAULT
                return False
            elif answer in entered_answers:
                print YELLOW + "You have already entered this answer" + DEFAULT
                return False
    return True

def print_answers(answers):
    print "ANSWERS:"
    for index in range (0, len(answers)):
        print "%d. %s" % (index + 1, answers[index])

def print_header(header):
    print "\n" + BLUE + "-----" + header + "-----" + DEFAULT

def write_to_txt(study_guide_id):
    study_guide_name = db_tools.get_study_guide_name(study_guide_id)
    study_guide_text = study_guide_name + "\n\n"
    questions = db_tools.get_questions_from_study_guide(study_guide_id)

    for i in range(0, len(questions)):
        question_id, question_text = questions[i]
        study_guide_text += "%d. %s\n" % (i + 1, question_text)
        answers = db_tools.get_answers_of_question(question_id)
        for j in range(0, len(answers)):
            study_guide_text += "\t%d. %s\n" % (j + 1, answers[j])
    file_name = "study_guide_%s.txt" % study_guide_name.lower().replace(" ", "_")
    file = open(file_name, "w")
    file.write(study_guide_text)
    file.close()

    print "%s written successfully" % file_name

# ******** MAIN ********
if __name__ == '__main__':
    try:
        user_menu()
    except SystemExit:
        raise
    except Exception:
        print YELLOW + "Whoops! An error has occurred. Exiting." + DEFAULT
        quit()
    except KeyboardInterrupt:
        print YELLOW + "\nExiting." + DEFAULT
        quit()
