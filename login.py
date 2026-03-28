# =============================================================
#  LOGIN MODULE
#  Admin/Teacher login via username+password
#  Student login via StudentID + Name
# =============================================================

from db import connect, hash_password
from utils import header, pause, masked_input


class LoginModule:

    def admin_teacher_login(self):
        """Login for Admin or Teacher. Returns (role, username) or (None, None)."""
        header("Admin / Teacher Login")
        username = input("  Enter Username : ").strip()
        password = masked_input("  Enter Password : ")

        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT role, full_name FROM users WHERE username=%s AND password=%s",
            (username, hash_password(password))
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            print(f"\n  \033[1;32mLogin successful! Welcome, {row[1]} ({row[0].upper()})\033[0m")
            pause()
            return row[0], username
        else:
            print("\n  \033[1;31mInvalid username or password.\033[0m")
            pause()
            return None, None

    def student_login(self):
        """Login for Student using Student_ID + Name (case-insensitive)."""
        header("Student Login")
        sid  = input("  Enter your Student ID : ").strip()
        name = input("  Enter your Name       : ").strip()

        conn = connect()
        cur  = conn.cursor()
        # FIX: Case-insensitive name comparison using LOWER()
        cur.execute(
            "SELECT student_id, name FROM students WHERE student_id=%s AND LOWER(name)=LOWER(%s)",
            (sid, name)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            print(f"\n  \033[1;32mWelcome, {row[1]}!\033[0m")
            pause()
            return row[0]
        else:
            print("\n  \033[1;31mInvalid Student ID or Name.\033[0m")
            pause()
            return None
