# Digital Library Manager

A multi-user Flask web application for managing personal book collections.

## Overview

Digital Library Manager allows users to create and manage their own personal book library. Each user can register, log in, add books, update reading progress, mark favorite books, search and filter their collection, and view book details with English summaries.

The application uses Flask, SQLite, raw SQL queries, and session-based authentication.

## Features

- User registration, login and logout
- Session-based authentication
- Multi-user book collection management
- Add, view, edit and delete books
- Favorite and unfavorite books
- Search books by title
- Filter books by category, status, favorites and top-rated books
- Reading statistics dashboard
- Recently added books section
- Book detail page with English summaries
- Modern dark library-themed UI

## User Stories

The project user stories and acceptance criteria are managed in the GitHub Projects Kanban Board.

Main user stories:

- US1 - Add Books to Personal Library
- US2 - Manage Book Collection
- US3 - Search and Filter Books
- US4 - Favorite Books
- US5 - View Reading Dashboard
- US6 - View Book Details and Summaries

## Technologies Used

- Python
- Flask
- SQLite
- Raw SQL
- HTML
- CSS
- Git
- GitHub Projects

## Database Structure

The application uses two main tables:

- `users`: stores registered user information
- `books`: stores book records linked to users with `user_id`

Each book belongs to one user. Users can only view and manage their own books.

## Installation

Install Flask:

```bash
pip install flask
```

## Run Project

Start the Flask application:

```bash
python app.py
```

Then open:

```plaintext
http://127.0.0.1:5000
```

## Project Structure

```plaintext
digital-library-manager/
│
├── app.py
├── book_data.py
├── database.py
├── logic.py
├── schema.sql
├── README.md
│
├── templates/
│   ├── add_book.html
│   ├── book_detail.html
│   ├── books.html
│   ├── dashboard.html
│   ├── edit_book.html
│   ├── home.html
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
└── tests/
    └── test_books.py
```

## Testing

Basic unit tests are included for business logic functions.

The tests cover:
- Getting book data from the predefined book list
- Calculating average rating
- Checking whether a book is top-rated

Routes are not tested directly, following the project requirements.

Run tests with:

```bash
python -m pytest
```

## Author

Mehmet Ali Öter
