# =============================================================
#  MODULE 2: ATTENDANCE MODULE
# =============================================================

import datetime
from db import connect
from utils import header, pause, divider


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

        # Validate date format
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
