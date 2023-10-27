## Goal Planner and Keeper System

Follow the steps below to set up and run the code:

### 1. Setup Environment:

Ensure you have **Python** and **pip** installed on your system. If you're using virtual environments (recommended), initiate one:
```
python -m venv venv
```
Activate the virtual environment:

- **On Windows**:
```
venv\Scripts\activate
```

- **On macOS and Linux**:
```
source venv/bin/activate
```

### 2. Install Required Packages:

Navigate to the directory containing the project files and install the necessary packages:
```
pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Login Flask-Migrate
```

### 3. Initialize the Database:

Before you can run the application, you need to create the database:
```
# To initialize migrations directory
flask db init

# To create a migration script
flask db migrate

# To apply the migrations
flask db upgrade
```
These commands set up and apply the migrations, creating the required tables in your SQLite database (`goals.db`).

### 4. Run the Application:

Start the Flask application:
```
export FLASK_APP=app.py 
# On Windows, use 'set' instead of 'export'
export FLASK_ENV=development
flask run
```
This will start the Flask development server. You should be able to navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser and interact with the application.
