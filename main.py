import json
import os
from datetime import date, timedelta

DATA_FILE = "habits.json"


def load_habits():
    """Load saved habits from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_habits(habits):
    """Save habits to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(habits, file, indent=4)


def add_habit(habits, name):
    """Add a new habit."""
    name = name.strip()

    if not name:
        raise ValueError("Habit name cannot be empty.")

    if name in habits:
        raise ValueError("Habit already exists.")

    habits[name] = {"completed_dates": []}
    return habits


def complete_habit(habits, name, today=None):
    """Mark a habit as completed for a particular date."""
    if name not in habits:
        raise ValueError("Habit does not exist.")

    if today is None:
        today = date.today()

    completed_dates = habits[name]["completed_dates"]
    today_string = today.isoformat()

    if today_string not in completed_dates:
        completed_dates.append(today_string)

    return habits


def calculate_streak(habits, name, today=None):
    """Calculate the current consecutive-day streak."""
    if name not in habits:
        raise ValueError("Habit does not exist.")

    if today is None:
        today = date.today()

    completed_dates = set(habits[name]["completed_dates"])
    streak = 0
    current_day = today

    while current_day.isoformat() in completed_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def main():
    """Run the command-line habit tracker."""
    habits = load_habits()

    while True:
        print("\n=== Habit Streak Tracker ===")
        print("1. Add habit")
        print("2. Complete habit")
        print("3. View habits and streaks")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter habit name: ")

            try:
                add_habit(habits, name)
                save_habits(habits)
                print("Habit added successfully.")
            except ValueError as error:
                print(error)

        elif choice == "2":
            name = input("Enter habit name: ")

            try:
                complete_habit(habits, name)
                save_habits(habits)
                print("Habit marked as completed today.")
            except ValueError as error:
                print(error)

        elif choice == "3":
            if not habits:
                print("No habits added yet.")
            else:
                for name in habits:
                    streak = calculate_streak(habits, name)
                    print(f"{name}: {streak}-day streak")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()