# Python Library Management System

A menu-driven Library Management System developed using Python and Object-Oriented Programming (OOP). The application provides dedicated Admin and Member portals to manage library operations, including books, memberships, circulation, reservations, and fines.

The project demonstrates practical Python programming through modular architecture, file handling, data validation, exception handling, and JSON-based data persistence.

## Features

### Admin Portal

- Admin login and account security management
- Update admin profile details and password
- Register, view, update, delete, and block/unblock members
- Add, search, update, and delete books
- Manage book categories
- Issue and return books
- Manage book reservations
- View unpaid fines and record payments
- Monitor overdue books
- Access dashboards, reports, and activity logs
- Back up and restore application data

### Member Portal

- Create a member account and log in
- View and update profile details
- Search for books
- Reserve books
- Issue and return books
- View issued and reserved books
- Pay fines
- View fine payment history

## Validation and Security Features

### Unique Identity and Duplicate Checking

- Automatically generate unique IDs for administrators, members, and books.
- Check username availability during member registration.
- Prevent registration with an already registered username.
- Check for duplicate email addresses and phone numbers.
- Display appropriate validation messages when duplicate information is entered.

### Email and Phone Number Validation

- Validate email addresses against the expected email format.
- Validate phone numbers against the required format.
- Reject invalid inputs and display appropriate error messages.

### Password Validation

Passwords must meet the following requirements:

- Minimum length of 8 characters
- At least one letter
- At least one number
- At least one symbol

The system validates password requirements before accepting a password.

## Technologies Used

- **Python** — core application logic
- **Object-Oriented Programming (OOP)** — classes and reusable code
- **File I/O** — reading from and writing to files
- **JSON** — structured data storage and persistence
- **Python Standard Library** — file handling, random ID generation, and date/time operations
- **Exception Handling** — handling errors and invalid operations
- **Python Data Structures** — organizing and managing application data

## Project Structure

```text
Python Library Management System/
│
├── main.py
├── .gitignore
├── README.md
│
├── admin_panel/
│   └── Admin-related feature modules
│
├── member_panel/
│   └── Member-related feature modules
│
├── core/
│   ├── admin_base.py
│   ├── member_base.py
│   └── book_model.py
│
└── database/
    ├── admins.json
    ├── members.json
    └── books.json
```

_Note: The admin and member panel directories contain separate Python modules for their respective features._

## How to Run

1. Install Python 3.
2. Open the project in Visual Studio Code or another Python-compatible editor.
3. Ensure the required JSON database files are present in the `database/` directory.
4. Run `main.py` using the editor's Run option.
5. Follow the on-screen menu to access the Admin or Member Portal.
6. **Admin Portal Access:** Admin registration is not available through the application. To access the Admin Portal, enter an existing admin username, Admin ID, and password. These credentials can be found in the `database/admins.json` file.

## Key Concepts Demonstrated

- Object-Oriented Programming
- Modular programming and code organization
- File I/O and JSON data persistence
- Data structures and data management
- Input validation and duplicate detection
- Unique ID generation
- Exception handling
- Menu-driven application design
- Library management workflows

## Data Storage

The application uses JSON files to store administrator, member, and book records. File handling operations allow the application to read existing data and save changes for subsequent use.

Keep the required database files in the `database/` directory to ensure the application can access its stored records.

## Sample Data Disclaimer

The JSON files in the `database/` directory contain dummy sample data provided solely for testing and demonstration purposes. This data is fictional and does not represent or relate to any real individuals or actual records.

Please use sample data for testing and replace it with your own appropriate test data when needed.

## Project Purpose

This project demonstrates the practical application of Python fundamentals and software development concepts through a structured, feature-rich Library Management System.

---

**Author:** Talib Akram
