# =============================================================
#  MODULE 1: STUDENT MANAGEMENT (Admin/Teacher)
# =============================================================

from db import connect
from utils import header, pause, divider, safe_str


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
            (sid, name, int(age) if age else None,
             gender or None, course or None, phone or None, address or None)
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

        # FIX: Use safe_str() to handle None values gracefully
        print(f"\n  {'ID':<12} {'Name':<22} {'Age':>4} {'Gender':<8} {'Course':<20} {'Phone':<14} {'Address'}")
        divider()
        for r in rows:
            print(f"  {safe_str(r[0]):<12} {safe_str(r[1]):<22} {safe_str(r[2], '-'):>4} "
                  f"{safe_str(r[3], '-'):<8} {safe_str(r[4], '-'):<20} "
                  f"{safe_str(r[5], '-'):<14} {safe_str(r[6], '-')}")
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

        # FIX: Display safe values instead of raw None
        print(f"\n  Existing -> Name: {safe_str(row[1])}  Age: {safe_str(row[2], '-')}  Course: {safe_str(row[4], '-')}")
        print("  (Press Enter to keep existing value)\n")

        name    = input(f"  Name    [{safe_str(row[1])}]: ").strip() or row[1]
        age     = input(f"  Age     [{safe_str(row[2], '-')}]: ").strip()
        gender  = input(f"  Gender  [{safe_str(row[3], '-')}]: ").strip() or row[3]
        course  = input(f"  Course  [{safe_str(row[4], '-')}]: ").strip() or row[4]
        phone   = input(f"  Phone   [{safe_str(row[5], '-')}]: ").strip() or row[5]
        address = input(f"  Address [{safe_str(row[6], '-')}]: ").strip() or row[6]

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
