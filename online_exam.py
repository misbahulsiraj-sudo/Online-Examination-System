import json
import os
import random
import time
import hashlib


RESULT_FILE = "exam_results.json"
EXAM_DURATION = 60  # seconds


# -------------------------------------------------
# Question Bank
# -------------------------------------------------

QUESTIONS = [
    {
        "question": "Which language is mainly used for AI and Machine Learning?",
        "options": ["Java", "Python", "HTML", "CSS"],
        "answer": 2
    },
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Control Processing Unit"
        ],
        "answer": 1
    },
    {
        "question": "Which data type is used to store True or False?",
        "options": ["String", "Integer", "Boolean", "Float"],
        "answer": 3
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["//", "#", "/*", "--"],
        "answer": 2
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "define", "def", "fun"],
        "answer": 3
    },
    {
        "question": "What is the full form of RAM?",
        "options": [
            "Read Access Memory",
            "Random Access Memory",
            "Rapid Access Memory",
            "Run Access Memory"
        ],
        "answer": 2
    },
    {
        "question": "Which of the following is a Python collection?",
        "options": ["List", "Loop", "Function", "Operator"],
        "answer": 1
    },
    {
        "question": "Which device is used to input text into a computer?",
        "options": ["Monitor", "Printer", "Keyboard", "Speaker"],
        "answer": 3
    },
    {
        "question": "What is 10 + 5 in Python?",
        "options": ["15", "105", "10+5", "Error"],
        "answer": 1
    },
    {
        "question": "Which company developed the Windows operating system?",
        "options": ["Apple", "Google", "Microsoft", "IBM"],
        "answer": 3
    }
]


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def hash_password(password):
    """Convert password into a secure hash."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_results():
    """Load previous exam results from file."""
    if not os.path.exists(RESULT_FILE):
        return []

    try:
        with open(RESULT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_result(result):
    """Save exam result to JSON file."""
    results = load_results()
    results.append(result)

    try:
        with open(RESULT_FILE, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)

    except OSError:
        print("\nUnable to save result.")


def calculate_grade(percentage):
    """Return grade based on percentage."""

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


# -------------------------------------------------
# Online Examination System
# -------------------------------------------------

class OnlineExam:

    def __init__(self):
        self.users = {}
        self.current_user = None

    # ---------------------------------------------
    # Registration
    # ---------------------------------------------

    def register(self):
        print("\n" + "=" * 55)
        print("                 STUDENT REGISTRATION")
        print("=" * 55)

        username = input("Create Username: ").strip()

        if not username:
            print("Username cannot be empty.")
            return

        if username in self.users:
            print("Username already exists.")
            return

        password = input("Create Password: ").strip()

        if len(password) < 4:
            print("Password must contain at least 4 characters.")
            return

        self.users[username] = hash_password(password)

        print("\nRegistration successful!")
        print("You can now login.")

    # ---------------------------------------------
    # Login
    # ---------------------------------------------

    def login(self):
        print("\n" + "=" * 55)
        print("                     STUDENT LOGIN")
        print("=" * 55)

        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username not in self.users:
            print("\nUser not found.")
            return False

        if self.users[username] != hash_password(password):
            print("\nIncorrect password.")
            return False

        self.current_user = username

        print(f"\nWelcome, {username}!")
        return True

    # ---------------------------------------------
    # Start Exam
    # ---------------------------------------------

    def start_exam(self):
        if not self.current_user:
            print("Please login first.")
            return

        questions = QUESTIONS.copy()
        random.shuffle(questions)

        score = 0
        answered = 0

        start_time = time.time()

        print("\n" + "=" * 60)
        print("                    ONLINE EXAM")
        print("=" * 60)
        print(f"Total Questions : {len(questions)}")
        print(f"Time Limit      : {EXAM_DURATION} seconds")
        print("=" * 60)

        input("\nPress Enter to start the exam...")

        start_time = time.time()

        for number, question in enumerate(questions, start=1):

            elapsed_time = time.time() - start_time
            remaining_time = EXAM_DURATION - int(elapsed_time)

            if remaining_time <= 0:
                print("\nTime is over!")
                break

            print("\n" + "-" * 60)
            print(f"Question {number}/{len(questions)}")
            print(f"Time Remaining: {remaining_time} seconds")
            print("-" * 60)

            print(question["question"])

            for index, option in enumerate(question["options"], start=1):
                print(f"{index}. {option}")

            while True:
                answer = input("Your Answer (1-4): ").strip()

                if answer in ["1", "2", "3", "4"]:
                    answer = int(answer)
                    break

                print("Please enter a number between 1 and 4.")

            answered += 1

            if answer == question["answer"]:
                score += 1

        self.show_result(
            score,
            len(questions),
            answered
        )

    # ---------------------------------------------
    # Show Result
    # ---------------------------------------------

    def show_result(self, score, total, answered):

        percentage = (score / total) * 100

        grade = calculate_grade(percentage)

        if percentage >= 40:
            status = "PASS"
        else:
            status = "FAIL"

        result = {
            "student": self.current_user,
            "score": score,
            "total": total,
            "answered": answered,
            "percentage": round(percentage, 2),
            "grade": grade,
            "status": status,
            "date": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        save_result(result)

        print("\n" + "=" * 60)
        print("                     EXAM RESULT")
        print("=" * 60)

        print(f"Student       : {self.current_user}")
        print(f"Questions     : {total}")
        print(f"Answered      : {answered}")
        print(f"Correct       : {score}")
        print(f"Incorrect     : {answered - score}")
        print(f"Percentage    : {percentage:.2f}%")
        print(f"Grade         : {grade}")
        print(f"Result        : {status}")

        print("=" * 60)

    # ---------------------------------------------
    # View Result History
    # ---------------------------------------------

    def view_results(self):

        if not self.current_user:
            print("Please login first.")
            return

        results = load_results()

        user_results = [
            result
            for result in results
            if result["student"] == self.current_user
        ]

        print("\n" + "=" * 70)
        print("                    RESULT HISTORY")
        print("=" * 70)

        if not user_results:
            print("No previous results found.")
            return

        for number, result in enumerate(user_results, start=1):

            print(f"\nAttempt {number}")
            print(f"Date       : {result['date']}")
            print(f"Score      : {result['score']}/{result['total']}")
            print(f"Percentage : {result['percentage']}%")
            print(f"Grade      : {result['grade']}")
            print(f"Status     : {result['status']}")
            print("-" * 70)

    # ---------------------------------------------
    # Logout
    # ---------------------------------------------

    def logout(self):
        print(f"\nGoodbye, {self.current_user}!")

        self.current_user = None


# -------------------------------------------------
# Main Program
# -------------------------------------------------

def main():

    exam_system = OnlineExam()

    while True:

        if exam_system.current_user is None:

            print("\n" + "=" * 60)
            print("              ONLINE EXAMINATION SYSTEM")
            print("=" * 60)
            print("1. Student Registration")
            print("2. Student Login")
            print("3. Exit")
            print("=" * 60)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                exam_system.register()

            elif choice == "2":
                exam_system.login()

            elif choice == "3":
                print("\nThank you for using Online Examination System!")
                break

            else:
                print("\nInvalid choice.")

        else:

            print("\n" + "=" * 60)
            print(f"              WELCOME, {exam_system.current_user}")
            print("=" * 60)
            print("1. Start Exam")
            print("2. View Result History")
            print("3. Logout")
            print("=" * 60)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                exam_system.start_exam()

            elif choice == "2":
                exam_system.view_results()

            elif choice == "3":
                exam_system.logout()

            else:
                print("\nInvalid choice.")


# -------------------------------------------------
# Program Entry Point
# -------------------------------------------------

if __name__ == "__main__":
    main()