
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
