# =============================================================
#  MODULE 5: USER MANAGEMENT (Admin only)
# =============================================================

from db import connect, hash_password
from utils import header, pause, divider, masked_input


class UserModule:

    # ── ADD USER ───────────────────────────────────────────
    def add_user(self):
        header("Add New User (Admin/Teacher)")

        uname    = input("  Username  : ").strip()
        password = masked_input("  Password  : ")
        fname    = input("  Full Name : ").strip()
        role     = input("  Role (admin/teacher): ").strip().lower()

        if role not in ("admin", "teacher"):
            print("  Role must be 'admin' or 'teacher'.")
            return

        if not uname or not password or not fname:
            print("  All fields are required.")
            return

        if len(password) < 4:
            print("  Password must be at least 4 characters long.")
            return

        conn = connect()
        cur  = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=%s", (uname,))
        if cur.fetchone():
            print(f"\n  Username '{uname}' already exists.")
            cur.close(); conn.close(); return

        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (%s,%s,%s,%s)",
            (uname, hash_password(password), fname, role)
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
        old_pass = masked_input("  Enter Old Password      : ")
        new_pass = masked_input("  Enter New Password      : ")
        confirm  = masked_input("  Confirm New Password    : ")

        if new_pass != confirm:
            print("  Passwords do not match.")
            return

        if len(new_pass) < 4:
            print("  Password must be at least 4 characters long.")
            return

        conn = connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT user_id FROM users WHERE username=%s AND password=%s",
            (uname, hash_password(old_pass))
        )
        if not cur.fetchone():
            print("  Incorrect username or old password.")
            cur.close(); conn.close(); return

        cur.execute("UPDATE users SET password=%s WHERE username=%s", (hash_password(new_pass), uname))
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
