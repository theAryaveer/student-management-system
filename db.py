# ─────────────────────────────────────────────
#  DATABASE LAYER
# ─────────────────────────────────────────────

import hashlib
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def hash_password(plain):
    """Hash a password using SHA-256. Fixes plain-text password storage."""
    return hashlib.sha256(plain.encode('utf-8')).hexdigest()


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
            password    VARCHAR(100) NOT NULL,
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

    # ── seed default admin (password hashed) ──
    cur.execute("SELECT user_id FROM users WHERE username = 'admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (%s,%s,%s,%s)",
            ("admin", hash_password("admin123"), "Administrator", "admin")
        )

    # ── seed default teacher (password hashed) ──
    cur.execute("SELECT user_id FROM users WHERE username = 'teacher1'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (%s,%s,%s,%s)",
            ("teacher1", hash_password("teach123"), "Teacher One", "teacher")
        )

    raw.commit()
    cur.close()
    raw.close()
