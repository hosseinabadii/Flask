# Flask Blog Project

Welcome to the repository for My Flask Blog Project, a dynamic blogging platform where users can register, create, and manage their posts. This platform is built with Flask, a micro web framework written in Python.

## Features

- **User Authentication**: Utilizes Flask-Login for user registration and authentication.
- **User Roles**: Supports two user roles with distinct permissions:
  - **Author**: Default role for new users, allowing them to create, edit, and delete their own posts.
  - **Administrator**: Full access to the admin panel, user management, and CRUD operations on all posts.
- **Admin Panel**: Powered by Flask-Admin for easy administration of the website.
- **Public Posts**: Posts marked as public are displayed on the index page for everyone to read.
- **Personal Post Management**: Users can manage their own posts - edit or delete them.
- **Database**: SQLite with the support of Flask-SQLAlchemy and SQLAlchemy.

## Installation

To set up and run the blog platform locally, follow these steps:

1. Clone the Repository

2. Create a Virtual Environment

3. Install Dependencies

```bash
pip install -r requirements.txt
```

5. Run the Application

```bash
python src/run.py
```

The application should now be running on [http://localhost:5000](http://localhost:5000).

## Usage

After launching the app, you can:

- Register a new user account.
- Log in with your user credentials.
- Create new posts and manage existing ones.
- If you have the administrator role, access the admin panel at `/admin`.

**Note**: To change a user's role to 'Administrator', do so directly by editing the role in the SQLite database.

## Experience Our Flask Blogging Platform

To visit the online demo of this application, [click here](https://khosro.pythonanywhere.com/).

## Configuration

Before running the application, you might want to set the environment variables for your Flask app. You can do this by completing the `env.txt` file in the root directory and renaming it to `.env`

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

## Acknowledgments

- Flask
- Flask-Login
- Flask-Admin
- Flask-SQLAlchemy
- SQLAlchemy
