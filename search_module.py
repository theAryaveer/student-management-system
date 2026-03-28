# =============================================================
#  MODULE 4: SEARCH & FILTER
# =============================================================

from db import connect
from utils import header, divider, safe_str


def escape_like(value):
    """Escape LIKE wildcard characters (% and _) in user input.
    Fixes Issue #5: prevents unintended pattern matching."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


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
            escaped = escape_like(val)
            cur.execute(
                "SELECT * FROM students WHERE student_id LIKE %s ESCAPE '\\\\'",
                (f"%{escaped}%",)
            )
        elif ch == "2":
            val = input("  Enter Name (partial ok): ").strip()
            escaped = escape_like(val)
            cur.execute(
                "SELECT * FROM students WHERE name LIKE %s ESCAPE '\\\\'",
                (f"%{escaped}%",)
            )
        elif ch == "3":
            val = input("  Enter Course (partial ok): ").strip()
            escaped = escape_like(val)
            cur.execute(
                "SELECT * FROM students WHERE course LIKE %s ESCAPE '\\\\'",
                (f"%{escaped}%",)
            )
        else:
            print("  Invalid choice.")
            cur.close(); conn.close(); return

        rows = cur.fetchall()
        cur.close(); conn.close()

        if not rows:
            print("\n  No matching records found.")
            return

        # FIX (Issue #7): Use safe_str() to handle None values
        print(f"\n  {'ID':<12} {'Name':<22} {'Age':>4} {'Gender':<8} {'Course':<20} {'Phone':<14} {'Address'}")
        divider()
        for r in rows:
            print(f"  {safe_str(r[0]):<12} {safe_str(r[1]):<22} {safe_str(r[2], '-'):>4} "
                  f"{safe_str(r[3], '-'):<8} {safe_str(r[4], '-'):<20} "
                  f"{safe_str(r[5], '-'):<14} {safe_str(r[6], '-')}")
        divider()
        print(f"\n  {len(rows)} record(s) found.")
