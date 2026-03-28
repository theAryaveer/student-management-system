# =============================================================
#        STUDENT MANAGEMENT SYSTEM
#   Language      : Python 3
#   Database      : MySQL
#   Concepts      : OOP, CRUD, Login System, Role-Based Access
# =============================================================
#
#  HOW TO RUN
#  ----------
#  1. Install connector  :  pip install mysql-connector-python
#  2. Set your MySQL password in config.py -> DB_PASSWORD
#  3. Run                :  python main.py
#
#  DEFAULT LOGINS
#  --------------
#  Admin   ->  username: admin      password: admin123
#  Teacher ->  username: teacher1   password: teach123
#  Student ->  Login with Student_ID + Name (case-insensitive)
#
#  PROJECT STRUCTURE
#  -----------------
#  config.py            - Database configuration
#  db.py                - Database connection & setup (with hashed passwords)
#  utils.py             - Helpers: banner, clear, masked_input, safe_str
#  login.py             - Login module (admin/teacher/student)
#  student_module.py    - Student CRUD operations
#  attendance_module.py - Attendance marking & reports
#  marks_module.py      - Marks entry & result display
#  search_module.py     - Search & filter with LIKE escaping
#  user_module.py       - User management (admin only)
#  student_portal.py    - Student self-service portal
#  menus.py             - Admin & Teacher dashboard menus
#  main.py              - Entry point (this file)
# =============================================================

from db import setup_database
from login import LoginModule
from menus import admin_menu, teacher_menu
from student_portal import StudentPortal
from utils import clear, banner, pause


def main():
    setup_database()
    login = LoginModule()

    while True:
        clear()
        banner()
        print()
        print("  \033[1;33m  WHO ARE YOU?\033[0m")
        print()
        print("  1. Admin Login")
        print("  2. Teacher Login")
        print("  3. Student Login")
        print("  4. Exit")
        print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
        ch = input("  Enter Choice: ").strip()

        if ch in ("1", "2"):
            role, uname = login.admin_teacher_login()
            if role == "admin" and ch == "1":
                admin_menu()
            elif role == "teacher" and ch == "2":
                teacher_menu()
            elif role == "admin" and ch == "2":
                print("\n  \033[1;31mYou are an Admin. Please use Admin Login.\033[0m")
                pause()
            elif role == "teacher" and ch == "1":
                print("\n  \033[1;31mYou are a Teacher. Please use Teacher Login.\033[0m")
                pause()
            # FIX (Issues #9, #10): Removed non-functional "Try again?" prompt.
            # The loop naturally returns to the main menu, which is the correct behavior.

        elif ch == "3":
            sid = login.student_login()
            if sid:
                portal = StudentPortal(sid)
                portal.menu()
            # FIX (Issue #10): Removed dead "Try again?" code — loop returns to menu.

        elif ch == "4":
            clear()
            banner()
            print("\n  \033[1;32m  Thank you! Goodbye.\033[0m\n")
            break

        else:
            print("  Invalid choice.")
            pause()


if __name__ == "__main__":
    main()
