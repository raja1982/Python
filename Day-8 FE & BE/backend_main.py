# ==============================
# execute this command on terminal : uvicorn backend_main:app --reload
# chk for port 8000 open in macbook => lsof -i :8000
# to kill the open port => kill -9 portnumber

# ==============================
# Install libraries
# ==============================
# ! pip install --quiet pydantic
# ! pip install --quiet fastapi uvicorn
# ! pip install --quiet email-validator

# ==============================
# Import required libraries
# ==============================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
import sqlite3

# ==============================
# Initialize FastAPI app
# ==============================
app = FastAPI(title="FastAPI Example with Pydantic & SQLite")

# ==============================
# Connect to SQLite Database
# (Creates a file 'users.db' if it doesn't exist)
# ==============================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# ==============================
# Create table for users (if not already present)
# ==============================
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL, email TEXT UNIQUE NOT NULL)
''')
conn.commit()

# ==============================
# STEP 1: Define a basic Python function to validate input
# (This is the "old way" — error-prone and verbose) ... this redundant function but can be used for additional checks
# ==============================
def validate_user_data_python(name, age, email):
    if not name or len(name) < 2:
        raise ValueError("Name must be at least 2 characters long.")
    if not isinstance(age, int) or age <= 0:
        raise ValueError("Age must be a positive integer.")
    if "@" not in email or "." not in email:
        raise ValueError("Invalid email format.")
    return True

# ==============================
# STEP 2: Define a Pydantic Model for Validation
# (This is the "new way" — cleaner and automatic)

# The moment FastAPI sees user: User in the function signature, it validates the incoming JSON against the User model before your function body even starts executing. If name is too short, age isn't a positive int, or email isn't a valid email — FastAPI/Pydantic rejects the request with a 422 Unprocessable Entity automatically, and register_user() never even runs.

# Explaination for 3 dots...
# age: int = Field(..., gt=0)        # required — client MUST send age
# age: int = Field(None, gt=0)       # optional — defaults to None if not sent

# email: EmailStr dtype checks that the text looks like a valid email address.
# ==============================
class User(BaseModel):
    name: str = Field(..., min_length=2, description="User's name must be at least 2 characters long")
    age: int = Field(..., gt=0, description="Age must be a positive integer")
    email: EmailStr  # Automatically validates email format

# ==============================
# STEP 3: Create an API endpoint
# ==============================
@app.get("/")
def root():
    return {"message": "API is running. Visit /docs to explore endpoints."}

@app.post("/register/")
def register_user(user: User):  # 'user' will be auto-validated by Pydantic
    """
    Registers a new user after validation.
    """

    # Option 1: Python validation (not needed, just for comparison)
    try:
        validate_user_data_python(user.name, user.age, user.email)
    except ValueError as e:
        # Normally we won't need this once Pydantic is in place
        raise HTTPException(status_code=400, detail=f"Python Validation Failed: {e}")

    # Option 2: Insert validated data into SQLite
    try:
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            (user.name, user.age, user.email)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists!")

    return {"message": "User registered successfully!", "user": user}

# ==============================
# STEP 4: Create a simple GET endpoint to see all users
# ==============================
@app.get("/users/")
def get_all_users():
    cursor.execute("SELECT id, name, age, email FROM users")
    users = cursor.fetchall()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found!")
    return {"users": users}

# ==============================
# STEP 5: Get a single user by ID
# (Used by the frontend to pre-fill the "Update User" form)
# ==============================
@app.get("/users/{user_id}")
def get_user(user_id: int):
    cursor.execute("SELECT id, name, age, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return {"id": user[0], "name": user[1], "age": user[2], "email": user[3]}

# ==============================
# STEP 6: Update an existing user (PUT)
# Notice we reuse the SAME 'User' Pydantic model used for registration —
# so the incoming data is validated automatically here too, before this
# function body runs (name length, age > 0, valid email format).
# ==============================
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    # 1. Make sure the user actually exists before trying to update it
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    existing = cursor.fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="User not found!")

    # 2. Attempt the update — email is UNIQUE, so updating to an email
    #    that belongs to another user will raise sqlite3.IntegrityError
    try:
        cursor.execute(
            "UPDATE users SET name = ?, age = ?, email = ? WHERE id = ?",
            (user.name, user.age, user.email, user_id)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already in use by another user!")

    return {"message": "User updated successfully!", "user": user}

# ==============================
# STEP 7: Delete a user (DELETE)
# ==============================
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # 1. Make sure the user actually exists before trying to delete it
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    existing = cursor.fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="User not found!")

    # 2. Delete the row
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    return {"message": f"User with id {user_id} deleted successfully!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_main:app", host="127.0.0.1", port=8000, reload=True)