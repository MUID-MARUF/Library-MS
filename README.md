# Library Management System (LMS)

A professional, high-performance Library Management System built with **Python Django** and **MySQL**. This application features a modern, interactive dashboard with a dual-theme UI, automated database operations, and deep-data relationship mapping.

---

## 🌟 Core Features

- **Dynamic Dashboard:** Real-time visualization of total books, active members, system issues, and average user ratings.
- **Automated Inventory Management:** Smart addition of books with automated ID generation, author lookup/creation, and category classification.
- **Relational Data Mapping:** Advanced SQL joining to reveal full details (Publisher, Category, Staff Roles) for every record.
- **Issue Tracking System:** Streamlined book issuing with automated date stamping and dropdown-based member/staff selection.
- **Dual-Theme Support:** Sleek UI with a persistent Dark Mode toggle for improved user experience.
- **Ratings & Reviews:** Integrated feedback system to monitor book popularity and member satisfaction.

---

## 🏗️ Technical Architecture

The system is designed with a strict separation of concerns to ensure maintainability and professional standards:

- **Frontend:** HTML5, Vanilla CSS3 (Custom Variables), and ES6+ JavaScript.
- **Backend:** Django 6.0 Framework.
- **Database:** MySQL (via XAMPP) using Raw SQL queries to maintain schema integrity and complex relationship management.
- **Database Engine:** A dedicated `db_operations.py` layer handles all CRUD operations independently from the views.

---

## 🚀 Installation & Setup

### 1. Database Initialization (XAMPP)
1. Launch **XAMPP Control Panel** and start the **Apache** and **MySQL** services.
2. Open **phpMyAdmin** (`http://localhost/phpmyadmin/`).
3. Create a new database named `library_db`.
4. Import the schema and initial data by running the code within `Library Management System.txt` in the SQL editor.

### 2. Environment Setup
1. Open your terminal in the project root directory.
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install necessary dependencies:
   ```bash
   pip install django mysql-connector-python
   ```

### 3. Launching the Application
1. Run the Django development server:
   ```bash
   python manage.py runserver 8001
   ```
2. Access the system in your web browser at:
   `http://127.0.0.1:8001/`

---

## 📁 Directory Structure

```text
├── library_project/      # Main configuration and routing
├── library_app/
│   ├── db_operations.py  # Core SQL Engine (The Engine)
│   ├── views.py          # Request Controllers (The Manager)
│   └── ...
├── static/
│   ├── css/              # Custom stylesheets & Dark Mode themes
│   └── js/               # Frontend logic & AJAX handlers
├── templates/            # HTML5 User Interface
└── README.md             # System documentation
```

---

## 🦅 The Falcons - Development Team

This project was engineered and maintained by **The Falcons**:

1. **Ridwan Hossain Taj** (592)
2. **Motasin Shahriar** (664)
3. **Sumiya Islam Mithila** (671)
4. **Any Akter** (181)
5. **A.K.M. Tahim Ibn Tazul Pranta** (977)

---
*© 2026 Library Management System - Powered by The Falcons.*
