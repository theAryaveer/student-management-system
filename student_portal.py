# =============================================================
#  STUDENT PORTAL (after student login)
# =============================================================

from db import connect
from utils import header, pause, divider, grade_from_percent, safe_str


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

        labels = ["Student ID", "Name", "Age", "Gender", "Course", "Phone", "Address"]
        print()
        for label, val in zip(labels, r):
            print(f"  {label:<14}: {safe_str(val, '-')}")

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
