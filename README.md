
# 🎓 Student Management System

A **Python + MySQL based CLI application** designed to manage students, attendance, marks, and users with **role-based access control**.

---

## 🚀 Features

* 🔐 **Secure Login System**

  * Admin, Teacher, and Student roles
  * Password hashing using SHA-256

* 👨‍🎓 **Student Management (CRUD)**

  * Add, update, delete, and view student records

* 📊 **Marks Management**

  * Add and view student marks
  * Automatic result display

* 📅 **Attendance System**

  * Mark and track attendance
  * Generate reports

* 🔍 **Search & Filter**

  * Safe SQL LIKE search with wildcard escaping

* 👤 **User Management (Admin Only)**

  * Create and manage system users

* 🧑‍💻 **Student Portal**

  * Students can view their profile, marks, and attendance

---

## 🧱 Project Structure

```
student-management-system/
│
├── config.py            # Database configuration
├── db.py                # DB connection + setup + hashing
├── utils.py             # Helper functions
├── login.py             # Login system
├── student_module.py    # Student CRUD
├── attendance_module.py # Attendance features
├── marks_module.py      # Marks management
├── search_module.py     # Search functionality
├── user_module.py       # User management
├── student_portal.py    # Student interface
├── menus.py             # Admin/Teacher menus
├── main.py              # Entry point
└── README.md            # Project documentation
```

---

## ⚙️ Requirements

* Python 3.x
* MySQL Server

### Install Dependency

```bash
pip install mysql-connector-python
```

---

## 🛠️ Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-link>
cd student-management-system
```

2. **Configure Database**

* Open `config.py`
* Set your MySQL credentials:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "student_mgmt"
```

3. **Run the Application**

```bash
python main.py
```

---

## 🔑 Default Login Credentials

| Role    | Username   | Password |
| ------- | ---------- | -------- |
| Admin   | admin      | admin123 |
| Teacher | teacher1   | teach123 |
| Student | Student_ID | Name     |

> ⚠️ Student login is **case-insensitive**

---

## 🔒 Security Features

* Passwords are stored using **SHA-256 hashing**
* No plain-text password storage
* Input validation for secure operations

---

## 🧠 Key Concepts Used

* Object-Oriented Programming (OOP)
* Modular Architecture
* CRUD Operations
* Role-Based Access Control (RBAC)
* Secure Authentication
* SQL Optimization & Safety

---

