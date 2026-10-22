"""Student Grade Manager - a terminal program with no external frameworks.

Data structure choice:
    students is a dict keyed by roll number -> {"name": str, "mark": number}
    A dict gives O(1) duplicate-roll-number checks (two students may share a
    name, but never a roll number), and insertion order is preserved for display.
"""

MAX_MARK = 100


def get_grade(mark):
    """Return the letter grade for a mark (boundaries are inclusive)."""
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "E"


def fmt(mark):
    """Format a mark without trailing .0."""
    return f"{mark:g}"


def read_roll_no(students):
    """Ask for a unique roll number made only of digits."""
    while True:
        roll = input("Enter roll number (numbers only): ").strip()
        if not roll:
            print("  Error: roll number cannot be empty.")
        elif not (roll.isascii() and roll.isdigit()):
            print("  Error: roll number must contain digits only (0-9). Please try again.")
        else:
            roll = str(int(roll))  # so "007" and "7" count as the same roll number
            if roll not in students:
                return roll
            print(f"  Error: roll number {roll} already exists "
                  f"({students[roll]['name']}). Use a different one.")


def read_name():
    """Ask for a non-empty name made of letters, spaces, dots, hyphens."""
    while True:
        name = input("Enter student name: ").strip()
        if not name:
            print("  Error: name cannot be empty.")
        elif not all(ch.isalpha() or ch in " .-'" for ch in name):
            print("  Error: name may contain only letters, spaces, '.', '-' and \"'\".")
        else:
            return name


def read_mark():
    """Ask for a mark between 0 and 100 until a valid one is entered."""
    while True:
        text = input(f"Enter mark (0-{MAX_MARK}): ").strip()
        try:
            mark = float(text)
        except ValueError:
            print("  Error: please enter a number.")
            continue
        if mark != mark or mark in (float("inf"), float("-inf")):
            print("  Error: please enter a valid number.")
        elif mark < 0:
            print("  Error: mark cannot be negative. Please recheck and re-enter.")
        elif mark > MAX_MARK:
            print(f"  Error: maximum mark is {MAX_MARK}. Please recheck and enter the correct mark.")
        else:
            return int(mark) if mark == int(mark) else round(mark, 2)


def read_confirmed_mark():
    """Read a mark, show it with its grade, and let the user re-enter it."""
    while True:
        mark = read_mark()
        while True:
            answer = input(f"  Mark entered: {fmt(mark)} (Grade {get_grade(mark)}). "
                           "Is this correct? (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return mark
            if answer in ("n", "no"):
                break
            print("  Error: please answer y or n.")


def add_student(students):
    """Collect one student's details and store them."""
    print("\n--- Add Student ---")
    roll = read_roll_no(students)
    name = read_name()
    mark = read_confirmed_mark()
    students[roll] = {"name": name, "mark": mark}
    print(f"Saved {name} (Roll {roll}): {fmt(mark)} - Grade {get_grade(mark)}")


def show_results(students):
    """Print the results table and class statistics."""
    if not students:
        print("\nNo students added yet. Choose 'Add' first.")
        return

    # Column widths adapt to the data so the table always lines up.
    roll_w = max(len("Roll No"), max(len(r) for r in students))
    name_w = max(len("Name"), max(len(s["name"]) for s in students.values()))
    mark_w = max(len("Mark"), max(len(fmt(s["mark"])) for s in students.values()))
    grade_w = len("Grade")

    headers = ["Roll No".ljust(roll_w), "Name".ljust(name_w),
               "Mark".rjust(mark_w), "Grade".center(grade_w)]
    header_line = " | ".join(headers)
    divider = "-+-".join("-" * len(h) for h in headers)

    print("\n" + "=" * len(header_line))
    print("STUDENT RESULTS".center(len(header_line)))
    print("=" * len(header_line))
    print(header_line)
    print(divider)
    for roll, data in students.items():
        print(" | ".join([roll.ljust(roll_w), data["name"].ljust(name_w),
                          fmt(data["mark"]).rjust(mark_w),
                          get_grade(data["mark"]).center(grade_w)]))
    print(divider)

    marks = [d["mark"] for d in students.values()]
    print(f"Total students : {len(marks)}")
    print(f"Class average  : {sum(marks) / len(marks):.2f}")
    print(f"Highest mark   : {fmt(max(marks))}")
    print(f"Lowest mark    : {fmt(min(marks))}")


def print_menu():
    print("\n===== Student Grade Manager =====")
    print("  1. Add a student")
    print("  2. Show results")
    print("  3. Quit")


def main():
    students = {}
    actions = {
        "1": add_student, "add": add_student, "a": add_student,
        "2": show_results, "show": show_results, "s": show_results,
    }
    while True:
        print_menu()
        try:
            choice = input("Choose an option: ").strip().lower()
            if choice in ("3", "quit", "q"):
                print("Goodbye!")
                break
            action = actions.get(choice)
            if action is None:
                print("  Invalid choice. Enter 1 (add), 2 (show) or 3 (quit).")
            else:
                action(students)
        except (KeyboardInterrupt, EOFError):
            print("\nInput closed. Goodbye!")
            break


if __name__ == "__main__":
    main()