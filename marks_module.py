# =============================================================
#  MODULE 3: MARKS / RESULT MODULE
# =============================================================

from db import connect
from utils import header, pause, divider, grade_from_percent


class MarksModule:

    # ── ADD MARKS ──────────────────────────────────────────
    def add_marks(self):
        header("Add Marks")

        sid     = input("  Enter Student ID : ").strip()
        subject = input("  Enter Subject    : ").strip()
        marks_input = input("  Enter Marks      : ").strip()

        # FIX (Issue #4): Use try/except instead of broken string replace check
        # Old code: marks.replace(".", "").isdigit() would pass "1.2.3"
        try:
            marks = float(marks_input)
        except ValueError:
            print("  Marks must be a valid number.")
            return

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
            "SELECT s.student_id, s.name, COUNT(m.result_id), "
            "COALESCE(SUM(m.marks), 0), COALESCE(AVG(m.marks), 0) "
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
            total = float(r[3])
            avg   = float(r[4])
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
