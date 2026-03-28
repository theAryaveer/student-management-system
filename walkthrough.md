# Student Management System — Refactoring Walkthrough

## What Changed

Split 1 monolithic file (1030 lines) → **12 modular files**, and fixed all 12 reported issues.

## New Project Structure

```
student management system/
├── config.py                # DB credentials (1 place to edit)
├── db.py                    # Connection + setup + password hashing
├── utils.py                 # Helpers: banner, clear, masked_input, safe_str
├── login.py                 # LoginModule class
├── student_module.py        # StudentModule class (CRUD)
├── attendance_module.py     # AttendanceModule class
├── marks_module.py          # MarksModule class
├── search_module.py         # SearchModule class + LIKE escaping
├── user_module.py           # UserModule class (admin only)
├── student_portal.py        # StudentPortal class
├── menus.py                 # admin_menu() + teacher_menu()
├── main.py                  # Entry point (run this)
└── student_management.py    # OLD file (can be deleted)
```

## All 12 Issues Fixed

| # | Issue | Fix | File |
|---|---|---|---|
| 1 | 🔴 `"1.2.3"` crashes `float()` in add_marks | Replaced `str.replace().isdigit()` with `try/except float()` | [marks_module.py](file:///c:/Users/HP/Desktop/student%20management%20system/marks_module.py#L18-L22) |
| 2 | 🟡 `None` displays as text in view_students | Added `safe_str()` utility | [utils.py](file:///c:/Users/HP/Desktop/student%20management%20system/utils.py#L35-L39) |
| 3 | 🟡 `None` shows in update prompts | Used `safe_str()` in all prompts | [student_module.py](file:///c:/Users/HP/Desktop/student%20management%20system/student_module.py#L83-L93) |
| 4 | 🟡 "Try again?" non-functional (admin/teacher) | Removed dead code; loop naturally returns to menu | [main.py](file:///c:/Users/HP/Desktop/student%20management%20system/main.py#L68-L69) |
| 5 | 🟡 "Try again?" non-functional (student) | Same fix | [main.py](file:///c:/Users/HP/Desktop/student%20management%20system/main.py#L73-L74) |
| 6 | 🟢 LIKE wildcards `%` and `_` not escaped | Added `escape_like()` + SQL `ESCAPE` clause | [search_module.py](file:///c:/Users/HP/Desktop/student%20management%20system/search_module.py#L10-L13) |
| 7 | 🟢 Plain-text passwords in DB | SHA-256 hashing via `hash_password()` | [db.py](file:///c:/Users/HP/Desktop/student%20management%20system/db.py#L9-L11) |
| 8 | 🟡 `None` in search results display | Used `safe_str()` in search output | [search_module.py](file:///c:/Users/HP/Desktop/student%20management%20system/search_module.py#L56-L60) |
| 9 | 🟢 Case-sensitive student login | Added `LOWER()` comparison | [login.py](file:///c:/Users/HP/Desktop/student%20management%20system/login.py#L47-L49) |
| 10 | 🟢 No password length validation | Added 4-char minimum in user creation/change | [user_module.py](file:///c:/Users/HP/Desktop/student%20management%20system/user_module.py#L33-L35) |
| 11 | 🟢 `None` in student portal profile | Used `safe_str()` | [student_portal.py](file:///c:/Users/HP/Desktop/student%20management%20system/student_portal.py#L28) |
| 12 | ⭐ Password shows as stars | Custom `masked_input()` using `msvcrt` (Windows) | [utils.py](file:///c:/Users/HP/Desktop/student%20management%20system/utils.py#L41-L85) |

## Additional Improvements

- **SQL `COALESCE`** in `view_all_results` to avoid `None` arithmetic
- **Password column** widened to `VARCHAR(100)` to store SHA-256 hex digests
- **Empty string → None** conversion when inserting students (cleaner DB)

## How to Run

```bash
# Entry point is now main.py (not student_management.py)
python main.py
```

> [!IMPORTANT]
> Since passwords are now hashed, if you had existing users in the database with plain-text passwords, they won't be able to login. You have two options:
> 1. **Drop the database** and let `setup_database()` recreate it with hashed defaults: `DROP DATABASE student_mgmt;`
> 2. Or manually update existing passwords in MySQL using the SHA-256 hash.

## Verification

✅ All 12 Python files pass syntax compilation (`py_compile`) with zero errors.
