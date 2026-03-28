# =============================================================
#        STUDENT MANAGEMENT SYSTEM
#   Inspired from : Hostel Accommodation Management (C++)
#   Language      : Python 3
#   Database      : MySQL
#   Concepts      : OOP, CRUD, Login System, Role-Based Access
# =============================================================
#
#  HOW TO RUN
#  ----------
#  1. Install connector  :  pip install mysql-connector-python
#  2. Set your MySQL password in DB_PASSWORD below
#  3. Run                :  python student_management.py
#
#  DEFAULT LOGINS
#  --------------
#  Admin   ->  username: admin      password: admin123
#  Teacher ->  username: teacher1   password: teach123
#  Student ->  Login with Student_ID + Name (same as C++ version)
# =============================================================

import mysql.connector
import os
import getpass          # masks password input (like _getch in C++)
import datetime

# ─────────────────────────────────────────────
#  CONFIGURATION  (change password here)
# ─────────────────────────────────────────────

DB_HOST     = "localhost"
DB_USER     = "root"
DB_PASSWORD = "thesharma"   # <-- change this
DB_NAME     = "student_mgmt"


# ─────────────────────────────────────────────
#  DATABASE  LAYER
# ─────────────────────────────────────────────

def connect():
    """Return an open MySQL connection to student_mgmt."""
    return mysql.connector.connect(
        host     = DB_HOST,
        user     = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )


def setup_database():
    """Create database + all tables + default admin/teacher accounts."""
    raw = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD
    )
    cur = raw.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cur.execute(f"USE {DB_NAME}")

    # ── users (admin & teachers login here) ──
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INT          AUTO_INCREMENT PRIMARY KEY,
            username    VARCHAR(30)  UNIQUE NOT NULL,
            password    VARCHAR(50)  NOT NULL,
            full_name   VARCHAR(100) NOT NULL,
            role        ENUM('admin','teacher') NOT NULL
        )
    """)

    # ── students ──
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id  VARCHAR(20)  PRIMARY KEY,
            name        VARCHAR(50)  NOT NULL,
            age         INT,
            gender      VARCHAR(10),
            course      VARCHAR(50),
            phone       VARCHAR(15),
            address     VARCHAR(150)
        )
    """)

    # ── attendance ──
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            att_id      INT          AUTO_INCREMENT PRIMARY KEY,
            student_id  VARCHAR(20)  NOT NULL,
            att_date    DATE         NOT NULL,
            status      ENUM('Present','Absent') NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
                ON DELETE CASCADE
        )
    """)

    # ── marks / results ──
    cur.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            result_id   INT          AUTO_INCREMENT PRIMARY KEY,
            student_id  VARCHAR(20)  NOT NULL,
            subject     VARCHAR(50)  NOT NULL,
            marks       FLOAT        NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
                ON DELETE CASCADE
        )
    """)

    # ── seed default admin ──
    cur.execute("SELECT user_id FROM users WHERE username = 'admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (%s,%s,%s,%s)",
            ("admin", "admin123", "Administrator", "admin")
        )

    # ── seed default teacher ──
    cur.execute("SELECT user_id FROM users WHERE username = 'teacher1'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (%s,%s,%s,%s)",
            ("teacher1", "teach123", "Teacher One", "teacher")
        )

    raw.commit()
    cur.close()
    raw.close()


# ─────────────────────────────────────────────
#  HELPER  UTILITIES
# ─────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("\033[1;33m" + "=" * 70 + "\033[0m")
    print("\033[1;34m" + "        STUDENT MANAGEMENT SYSTEM".center(70) + "\033[0m")
    print("\033[1;33m" + "=" * 70 + "\033[0m")

def header(title):
    clear()
    banner()
    print("\033[1;33m" + "=" * 70 + "\033[0m")
    print("\033[1;34m" + f"  {title.upper()}".center(70) + "\033[0m")
    print("\033[1;33m" + "=" * 70 + "\033[0m")

def pause():
    input("\n  Press Enter to continue...")

def divider():
    print("  " + "-" * 66)

def grade_from_percent(pct):
    if pct >= 90: return "A+"
    if pct >= 80: return "A"
    if pct >= 70: return "B"
    if pct >= 60: return "C"
    if pct >= 50: return "D"
    return "F"


# =============================================================
#  LOGIN  MODULE
#  Mirrors C++: Admin/Teacher login via username+password
#               Student login via StudentID + Name
# =============================================================

class LoginModule:

    def admin_teacher_login(self):
        """Login for Admin or Teacher. Returns (role, username) or (None,None)."""
        header("Admin / Teacher Login")
        username = input("  Enter Username : ").strip()
        password = getpass.getpass("  Enter Password : ")   # masked like _getch

        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT role, full_name FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            print(f"\n  \033[1;32mLogin successful! Welcome, {row[1]} ({row[0].upper()})\033[0m")
            pause()
            return row[0], username           # role, username
        else:
            print("\n  \033[1;31mInvalid username or password.\033[0m")
            pause()
            return None, None

    def student_login(self):
        """Login for Student using Student_ID + Name (like C++ student_login.h)."""
        header("Student Login")
        sid  = input("  Enter your Student ID : ").strip()
        name = input("  Enter your Name       : ").strip()

        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT student_id, name FROM students WHERE student_id=%s AND name=%s",
            (sid, name)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            print(f"\n  \033[1;32mWelcome, {row[1]}!\033[0m")
            pause()
            return row[0]           # student_id
        else:
            print("\n  \033[1;31mInvalid Student ID or Name.\033[0m")
            pause()
            return None


# =============================================================
#  MODULE 1 :  STUDENT  MANAGEMENT  (Admin/Teacher)
# =============================================================

class StudentModule:

    # ── ADD ────────────────────────────────────────────────
    def add_student(self):
        header("Add New Student")

        sid     = input("  Student ID  : ").strip()
        name    = input("  Name        : ").strip()
        age     = input("  Age         : ").strip()
        gender  = input("  Gender (M/F): ").strip()
        course  = input("  Course      : ").strip()
        phone   = input("  Phone       : ").strip()
        address = input("  Address     : ").strip()

        if not sid or not name:
            print("  Student ID and Name are required.")
            return

        if age and not age.isdigit():
            print("  Age must be a number.")
            return

        conn = connect()
        cur  = conn.cursor()

        cur.execute("SELECT student_id FROM students WHERE student_id=%s", (sid,))
        if cur.fetchone():
            print(f"\n  Student ID '{sid}' already exists.")
            cur.close(); conn.close(); return

        cur.execute(
            "INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (sid, name, int(age) if age else None, gender, course, phone, address)
        )
        conn.commit()
        print(f"\n  \033[1;32mStudent '{sid}' added successfully.\033[0m")
        cur.close(); conn.close()

    # ── VIEW ALL ───────────────────────────────────────────
    def view_students(self):
        header("All Students")

        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY student_id")
        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print("  No student records found.")
            return

        print(f"\n  {'ID':<12} {'Name':<22} {'Age':>4} {'Gender':<8} {'Course':<20} {'Phone':<14} {'Address'}")
        divider()
        for r in rows:
            print(f"  {r[0]:<12} {r[1]:<22} {str(r[2]):>4} {str(r[3]):<8} {str(r[4]):<20} {str(r[5]):<14} {r[6]}")
        divider()

    # ── UPDATE ─────────────────────────────────────────────
    def update_student(self):
        header("Update Student")

        sid = input("  Enter Student ID to update: ").strip()

        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM students WHERE student_id=%s", (sid,))
        row = cur.fetchone()

        if not row:
            print(f"\n  Student '{sid}' not found.")
            cur.close(); conn.close(); return

        print(f"\n  Existing -> Name: {row[1]}  Age: {row[2]}  Course: {row[4]}")
        print("  (Press Enter to keep existing value)\n")

        name    = input(f"  Name    [{row[1]}]: ").strip() or row[1]
        age     = input(f"  Age     [{row[2]}]: ").strip()
        gender  = input(f"  Gender  [{row[3]}]: ").strip() or row[3]
        course  = input(f"  Course  [{row[4]}]: ").strip() or row[4]
        phone   = input(f"  Phone   [{row[5]}]: ").strip() or row[5]
        address = input(f"  Address [{row[6]}]: ").strip() or row[6]

        age = int(age) if age and age.isdigit() else row[2]

        cur.execute(
            "UPDATE students SET name=%s, age=%s, gender=%s, course=%s, phone=%s, address=%s WHERE student_id=%s",
            (name, age, gender, course, phone, address, sid)
        )
        conn.commit()
        print(f"\n  \033[1;32mStudent '{sid}' updated successfully.\033[0m")
        cur.close(); conn.close()

    # ── DELETE ─────────────────────────────────────────────
    def delete_student(self):
        header("Delete Student")

        sid = input("  Enter Student ID to delete: ").strip()

        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT name FROM students WHERE student_id=%s", (sid,))
        row = cur.fetchone()

        if not row:
            print(f"\n  Student '{sid}' not found.")
            cur.close(); conn.close(); return

        confirm = input(f"  Confirm delete '{row[0]}' ? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("  Deletion cancelled.")
            cur.close(); conn.close(); return

        cur.execute("DELETE FROM students WHERE student_id=%s", (sid,))
        conn.commit()
        print(f"\n  \033[1;32mStudent '{sid}' deleted (attendance & marks also removed).\033[0m")
        cur.close(); conn.close()

    # ── MENU ───────────────────────────────────────────────
    def menu(self):
        while True:
            header("Student Management")
            print("  1. Add Student")
            print("  2. View All Students")
            print("  3. Update Student")
            print("  4. Delete Student")
            print("  5. Back")
            print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
            ch = input("  Enter Choice: ").strip()
            if   ch == "1": self.add_student()
            elif ch == "2": self.view_students()
            elif ch == "3": self.update_student()
            elif ch == "4": self.delete_student()
            elif ch == "5": break
            else: print("  Invalid choice.")
            pause()


# =============================================================
#  MODULE 2 :  ATTENDANCE  MODULE
# =============================================================

class AttendanceModule:

    # ── MARK ───────────────────────────────────────────────
    def mark_attendance(self):
        header("Mark Attendance")

        sid    = input("  Enter Student ID : ").strip()
        date   = input("  Enter Date (YYYY-MM-DD) [today]: ").strip()
        status = input("  Status (P = Present / A = Absent): ").strip().upper()

        if not date:
            date = str(datetime.date.today())

        if status == "P":
            status = "Present"
        elif status == "A":
            status = "Absent"
        else:
            print("  Invalid status. Use P or A.")
            return

        # Validate date format simply
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("  Invalid date format. Use YYYY-MM-DD.")
            return

        conn = connect()
        cur  = conn.cursor()

        # Check student exists
        cur.execute("SELECT name FROM students WHERE student_id=%s", (sid,))
        s = cur.fetchone()
        if not s:
            print(f"\n  Student '{sid}' not found.")
            cur.close(); conn.close(); return

        # Check duplicate attendance for same date
        cur.execute(
            "SELECT att_id FROM attendance WHERE student_id=%s AND att_date=%s",
            (sid, date)
        )
        if cur.fetchone():
            print(f"\n  Attendance for '{sid}' on {date} already marked.")
            cur.close(); conn.close(); return

        cur.execute(
            "INSERT INTO attendance (student_id, att_date, status) VALUES (%s,%s,%s)",
            (sid, date, status)
        )
        conn.commit()
        print(f"\n  \033[1;32m{s[0]} marked {status} on {date}.\033[0m")
        cur.close(); conn.close()

    # ── VIEW REPORT ────────────────────────────────────────
    def view_report(self):
        header("Attendance Report")

        sid = input("  Enter Student ID (or press Enter for ALL): ").strip()

        conn = connect()
        cur  = conn.cursor()

        if sid:
            cur.execute(
                "SELECT s.name, a.att_date, a.status "
                "FROM attendance a JOIN students s ON a.student_id=s.student_id "
                "WHERE a.student_id=%s ORDER BY a.att_date",
                (sid,)
            )
        else:
            cur.execute(
                "SELECT s.name, a.att_date, a.status "
                "FROM attendance a JOIN students s ON a.student_id=s.student_id "
                "ORDER BY a.student_id, a.att_date"
            )

        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print("  No attendance records found.")
            return

        total   = len(rows)
        present = sum(1 for r in rows if r[2] == "Present")
        absent  = total - present
        pct     = (present / total * 100) if total else 0

        print(f"\n  {'Name':<22} {'Date':<14} {'Status'}")
        divider()
        for r in rows:
            color = "\033[1;32m" if r[2] == "Present" else "\033[1;31m"
            print(f"  {r[0]:<22} {str(r[1]):<14} {color}{r[2]}\033[0m")
        divider()
        print(f"\n  Total: {total}  |  Present: {present}  |  Absent: {absent}  |  Attendance: {pct:.1f}%")

    # ── MENU ───────────────────────────────────────────────
    def menu(self):
        while True:
            header("Attendance Management")
            print("  1. Mark Attendance")
            print("  2. View Attendance Report")
            print("  3. Back")
            print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
            ch = input("  Enter Choice: ").strip()
            if   ch == "1": self.mark_attendance()
            elif ch == "2": self.view_report()
            elif ch == "3": break
            else: print("  Invalid choice.")
            pause()


# =============================================================
#  MODULE 3 :  MARKS / RESULT  MODULE
# =============================================================

class MarksModule:

    # ── ADD MARKS ──────────────────────────────────────────
    def add_marks(self):
        header("Add Marks")

        sid     = input("  Enter Student ID : ").strip()
        subject = input("  Enter Subject    : ").strip()
        marks   = input("  Enter Marks      : ").strip()

        if not marks.replace(".", "").isdigit():
            print("  Marks must be a number.")
            return

        marks = float(marks)
        if marks < 0 or marks > 100:
            print("  Marks must be between 0 and 100.")
            return

        conn = connect()
        cur  = conn.cursor()

        cur.execute("SELECT name FROM students WHERE student_id=%s", (sid,))
        s = cur.fetchone()
        if not s:
            print(f"\n  Student '{sid}' not found.")
            cur.close(); conn.close(); return

        # Check if marks for same subject already exist
        cur.execute(
            "SELECT result_id FROM marks WHERE student_id=%s AND subject=%s",
            (sid, subject)
        )
        if cur.fetchone():
            upd = input(f"  Marks for '{subject}' already exist. Update? (yes/no): ").strip().lower()
            if upd == "yes":
                cur.execute(
                    "UPDATE marks SET marks=%s WHERE student_id=%s AND subject=%s",
                    (marks, sid, subject)
                )
                conn.commit()
                print(f"\n  \033[1;32mMarks updated for {s[0]} in {subject}.\033[0m")
            cur.close(); conn.close(); return

        cur.execute(
            "INSERT INTO marks (student_id, subject, marks) VALUES (%s,%s,%s)",
            (sid, subject, marks)
        )
        conn.commit()
        print(f"\n  \033[1;32mMarks added for {s[0]} in {subject}.\033[0m")
        cur.close(); conn.close()

    # ── VIEW RESULT ────────────────────────────────────────
    def view_result(self):
        header("Student Result")

        sid = input("  Enter Student ID: ").strip()

        conn = connect()
        cur  = conn.cursor()

        cur.execute("SELECT name FROM students WHERE student_id=%s", (sid,))
        s = cur.fetchone()
        if not s:
            print(f"\n  Student '{sid}' not found.")
            cur.close(); conn.close(); return

        cur.execute(
            "SELECT subject, marks FROM marks WHERE student_id=%s ORDER BY subject",
            (sid,)
        )
        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print(f"\n  No marks found for '{s[0]}'.")
            return

        total  = sum(r[1] for r in rows)
        count  = len(rows)
        avg    = total / count
        grade  = grade_from_percent(avg)

        print(f"\n  Student  : {s[0]}  [{sid}]")
        print(f"  {'Subject':<30} {'Marks':>8}  {'Grade':>6}")
        divider()
        for r in rows:
            g = grade_from_percent(r[1])
            print(f"  {r[0]:<30} {r[1]:>8.1f}  {g:>6}")
        divider()
        print(f"  {'Total':<30} {total:>8.1f}")
        print(f"  {'Average':<30} {avg:>8.1f}  {grade:>6}")
        print(f"  {'Subjects':<30} {count:>8}")

    # ── VIEW ALL RESULTS ───────────────────────────────────
    def view_all_results(self):
        header("All Students Result Summary")

        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT s.student_id, s.name, COUNT(m.result_id), SUM(m.marks), AVG(m.marks) "
            "FROM students s LEFT JOIN marks m ON s.student_id=m.student_id "
            "GROUP BY s.student_id, s.name ORDER BY s.student_id"
        )
        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print("  No records found.")
            return

        print(f"\n  {'ID':<12} {'Name':<22} {'Subjects':>8} {'Total':>8} {'Average':>8} {'Grade':>6}")
        divider()
        for r in rows:
            subj  = r[2] or 0
            total = r[3] or 0
            avg   = r[4] or 0
            g     = grade_from_percent(avg) if subj else "-"
            print(f"  {r[0]:<12} {r[1]:<22} {subj:>8} {total:>8.1f} {avg:>8.1f} {g:>6}")
        divider()

    # ── MENU ───────────────────────────────────────────────
    def menu(self):
        while True:
            header("Marks / Result Management")
            print("  1. Add Marks for a Student")
            print("  2. View Result of a Student")
            print("  3. View All Students Result Summary")
            print("  4. Back")
            print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
            ch = input("  Enter Choice: ").strip()
            if   ch == "1": self.add_marks()
            elif ch == "2": self.view_result()
            elif ch == "3": self.view_all_results()
            elif ch == "4": break
            else: print("  Invalid choice.")
            pause()


# =============================================================
#  MODULE 4 :  SEARCH & FILTER
# =============================================================

class SearchModule:

    def search(self):
        header("Search & Filter Students")
        print("  1. Search by Student ID")
        print("  2. Search by Name")
        print("  3. Search by Course")
        print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
        ch = input("  Enter Choice: ").strip()

        conn = connect()
        cur  = conn.cursor()

        if ch == "1":
            val = input("  Enter Student ID: ").strip()
            cur.execute("SELECT * FROM students WHERE student_id LIKE %s", (f"%{val}%",))
        elif ch == "2":
            val = input("  Enter Name (partial ok): ").strip()
            cur.execute("SELECT * FROM students WHERE name LIKE %s", (f"%{val}%",))
        elif ch == "3":
            val = input("  Enter Course (partial ok): ").strip()
            cur.execute("SELECT * FROM students WHERE course LIKE %s", (f"%{val}%",))
        else:
            print("  Invalid choice.")
            cur.close(); conn.close(); return

        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print("\n  No matching records found.")
            return

        print(f"\n  {'ID':<12} {'Name':<22} {'Age':>4} {'Gender':<8} {'Course':<20} {'Phone':<14} {'Address'}")
        divider()
        for r in rows:
            print(f"  {r[0]:<12} {r[1]:<22} {str(r[2]):>4} {str(r[3]):<8} {str(r[4]):<20} {str(r[5]):<14} {r[6]}")
        divider()
        print(f"\n  {len(rows)} record(s) found.")


# =============================================================
#  MODULE 5 :  USER MANAGEMENT  (Admin only)
#  Mirrors the User class in main.cpp
# =============================================================

class UserModule:

    # ── ADD USER ───────────────────────────────────────────
    def add_user(self):
        header("Add New User (Admin/Teacher)")

        uname    = input("  Username  : ").strip()
        password = getpass.getpass("  Password  : ")
        fname    = input("  Full Name : ").strip()
        role     = input("  Role (admin/teacher): ").strip().lower()

        if role not in ("admin", "teacher"):
            print("  Role must be 'admin' or 'teacher'.")
            return

        if not uname or not password or not fname:
            print("  All fields are required.")
            return

        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=%s", (uname,))
        if cur.fetchone():
            print(f"\n  Username '{uname}' already exists.")
            cur.close(); conn.close(); return

        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (%s,%s,%s,%s)",
            (uname, password, fname, role)
        )
        conn.commit()
        print(f"\n  \033[1;32mUser '{uname}' ({role}) added successfully.\033[0m")
        cur.close(); conn.close()

    # ── VIEW USERS ─────────────────────────────────────────
    def view_users(self):
        header("All Users")

        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT user_id, username, full_name, role FROM users")
        rows = cur.fetchall()
        cur.close(); conn.close()

        print(f"\n  {'ID':>5}  {'Username':<20} {'Full Name':<25} {'Role'}")
        divider()
        for r in rows:
            print(f"  {r[0]:>5}  {r[1]:<20} {r[2]:<25} {r[3]}")
        divider()

    # ── DELETE USER ────────────────────────────────────────
    def delete_user(self):
        header("Delete User")

        uname = input("  Enter Username to delete: ").strip()

        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT full_name, role FROM users WHERE username=%s", (uname,))
        row = cur.fetchone()

        if not row:
            print(f"\n  User '{uname}' not found.")
            cur.close(); conn.close(); return

        if uname == "admin":
            print("  Cannot delete the default admin account.")
            cur.close(); conn.close(); return

        confirm = input(f"  Delete '{row[0]}' ({row[1]})? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("  Deletion cancelled.")
            cur.close(); conn.close(); return

        cur.execute("DELETE FROM users WHERE username=%s", (uname,))
        conn.commit()
        print(f"\n  \033[1;32mUser '{uname}' deleted.\033[0m")
        cur.close(); conn.close()

    # ── CHANGE PASSWORD ────────────────────────────────────
    def change_password(self):
        header("Change Password")

        uname    = input("  Enter Username          : ").strip()
        old_pass = getpass.getpass("  Enter Old Password      : ")
        new_pass = getpass.getpass("  Enter New Password      : ")
        confirm  = getpass.getpass("  Confirm New Password    : ")

        if new_pass != confirm:
            print("  Passwords do not match.")
            return

        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT user_id FROM users WHERE username=%s AND password=%s",
            (uname, old_pass)
        )
        if not cur.fetchone():
            print("  Incorrect username or old password.")
            cur.close(); conn.close(); return

        cur.execute("UPDATE users SET password=%s WHERE username=%s", (new_pass, uname))
        conn.commit()
        print(f"\n  \033[1;32mPassword updated for '{uname}'.\033[0m")
        cur.close(); conn.close()

    # ── MENU ───────────────────────────────────────────────
    def menu(self):
        while True:
            header("User Management  [Admin Only]")
            print("  1. Add User (Admin/Teacher)")
            print("  2. View All Users")
            print("  3. Delete User")
            print("  4. Change Password")
            print("  5. Back")
            print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
            ch = input("  Enter Choice: ").strip()
            if   ch == "1": self.add_user()
            elif ch == "2": self.view_users()
            elif ch == "3": self.delete_user()
            elif ch == "4": self.change_password()
            elif ch == "5": break
            else: print("  Invalid choice.")
            pause()


# =============================================================
#  STUDENT  PORTAL  (after student login)
#  Mirrors student_login.h menu()
# =============================================================

class StudentPortal:

    def __init__(self, sid):
        self.sid = sid

    def my_profile(self):
        header("My Profile")
        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM students WHERE student_id=%s", (self.sid,))
        r = cur.fetchone()
        cur.close(); conn.close()

        if not r:
            print("  Record not found.")
            return

        labels = ["Student ID","Name","Age","Gender","Course","Phone","Address"]
        print()
        for label, val in zip(labels, r):
            print(f"  {label:<14}: {val}")

    def my_attendance(self):
        header("My Attendance")
        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT att_date, status FROM attendance WHERE student_id=%s ORDER BY att_date",
            (self.sid,)
        )
        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print("  No attendance records found.")
            return

        total   = len(rows)
        present = sum(1 for r in rows if r[1] == "Present")
        absent  = total - present
        pct     = (present / total * 100) if total else 0

        print(f"\n  {'Date':<14} {'Status'}")
        divider()
        for r in rows:
            color = "\033[1;32m" if r[1] == "Present" else "\033[1;31m"
            print(f"  {str(r[0]):<14} {color}{r[1]}\033[0m")
        divider()
        print(f"\n  Present: {present} / {total}  ({pct:.1f}%)")

    def my_result(self):
        header("My Result")
        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT subject, marks FROM marks WHERE student_id=%s ORDER BY subject",
            (self.sid,)
        )
        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print("  No marks found.")
            return

        total = sum(r[1] for r in rows)
        avg   = total / len(rows)

        print(f"\n  {'Subject':<30} {'Marks':>8}  {'Grade':>6}")
        divider()
        for r in rows:
            g = grade_from_percent(r[1])
            print(f"  {r[0]:<30} {r[1]:>8.1f}  {g:>6}")
        divider()
        print(f"  {'Total':<30} {total:>8.1f}")
        print(f"  {'Average':<30} {avg:>8.1f}  {grade_from_percent(avg):>6}")

    def menu(self):
        while True:
            header("Student Portal")
            print("  1. My Profile")
            print("  2. My Attendance")
            print("  3. My Result / Marks")
            print("  4. Logout")
            print("\033[1;36m" + "  " + "=" * 66 + "\033[0m")
            ch = input("  Enter Choice: ").strip()
            if   ch == "1": self.my_profile()
            elif ch == "2": self.my_attendance()
            elif ch == "3": self.my_result()
            elif ch == "4":
                print("\n  Logging out...")
                pause()
                break
            else: print("  Invalid choice.")
            pause()


# =============================================================
#  ADMIN  MENU  (full access)
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
#  TEACHER  MENU  (limited access - no user management)
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


# =============================================================
#  ENTRY  POINT  -  MAIN MENU
#  Mirrors the outer login loop in main.cpp
# =============================================================

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
            elif role is None:
                retry = input("  Try again? (Y/N): ").strip().upper()
                if retry != "Y":
                    continue

        elif ch == "3":
            sid = login.student_login()
            if sid:
                portal = StudentPortal(sid)
                portal.menu()
            else:
                retry = input("  Try again? (Y/N): ").strip().upper()

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
