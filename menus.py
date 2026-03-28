# =============================================================
#  ADMIN & TEACHER MENUS
# =============================================================

from utils import header, pause
from student_module import StudentModule
from attendance_module import AttendanceModule
from marks_module import MarksModule
from search_module import SearchModule
from user_module import UserModule


# =============================================================
#  ADMIN MENU (full access)
# =============================================================

def admin_menu():
    student_mod  = StudentModule()
    attend_mod   = AttendanceModule()
    marks_mod    = MarksModule()
    search_mod   = SearchModule()
    user_mod     = UserModule()

    while True:
        header("Admin Dashboard")
        print("  1. Student Management")
        print("  2. Attendance Management")
        print("  3. Marks / Result Management")
        print("  4. Search & Filter Students")
        print("  5. User Management")
        print("  6. Logout")
        print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
        ch = input("  Enter Choice: ").strip()

        if   ch == "1": student_mod.menu()
        elif ch == "2": attend_mod.menu()
        elif ch == "3": marks_mod.menu()
        elif ch == "4": search_mod.search(); pause()
        elif ch == "5": user_mod.menu()
        elif ch == "6":
            print("\n  Logging out...")
            pause()
            break
        else: print("  Invalid choice."); pause()


# =============================================================
#  TEACHER MENU (limited access - no user management)
# =============================================================

def teacher_menu():
    student_mod = StudentModule()
    attend_mod  = AttendanceModule()
    marks_mod   = MarksModule()
    search_mod  = SearchModule()

    while True:
        header("Teacher Dashboard")
        print("  1. View All Students")
        print("  2. Attendance Management")
        print("  3. Marks / Result Management")
        print("  4. Search & Filter Students")
        print("  5. Logout")
        print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
        ch = input("  Enter Choice: ").strip()

        if   ch == "1": student_mod.view_students(); pause()
        elif ch == "2": attend_mod.menu()
        elif ch == "3": marks_mod.menu()
        elif ch == "4": search_mod.search(); pause()
        elif ch == "5":
            print("\n  Logging out...")
            pause()
            break
        else: print("  Invalid choice."); pause()
