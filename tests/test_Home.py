import pytest
import sqlite3
from Home import AddCustomer, LoginCustomer

# for me to test: pytest tests/test_Home.py -v

@pytest.fixture
def db():  # making a mock in memory database for my tests on my home page functions
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UserName TEXT NOT NULL,
            Password TEXT NOT NULL,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL,
            Phone TEXT NOT NULL
        )
    """)
    conn.commit()
    yield conn
    conn.close()

def test_add_customer_success(db):  # using the fake db we made in memory
    # first test function then fetch the details and make sure the insert was correct
    AddCustomer(db, "testuser", "pass123", "Bella", "Kreit", "b@gmail.com", "818")
    cur = db.cursor()
    cur.execute("SELECT FirstName FROM Customers WHERE UserName = 'testuser'")
    result = cur.fetchone()
    assert result is not None
    assert result[0] == "Bella"

def test_add_customer_empty_username(db):
    with pytest.raises(ValueError):  # should raise error because a field is empty
        AddCustomer(db, "", "pass123", "Bella", "Kreit", "b@gmail.com", "818")

def test_add_customer_empty_password(db):
    with pytest.raises(ValueError):   # should raise error because password field is empty
        AddCustomer(db, "testuser", "", "Bella", "Kreit", "b@gmail.com", "818")


def test_login_success(db):  # testing login function with the in memory db
    AddCustomer(db, "testuser", "pass123", "Bella", "Kreit", "b@gmail.com", "818")
    result = LoginCustomer(db, "testuser", "pass123")
    assert result is not None
    assert result[0] == "Bella"  # making sure it gives back the first name
    assert result[1] == "Kreit"  # making sure it gives correct last name too

def test_login_noUser(db):  # testing login function with no one with username
    AddCustomer(db, "testuser", "pass123", "Bella", "Kreit", "b@gmail.com", "818")
    with pytest.raises(ValueError, match="Username not found."):  # tests that the error is raised and it has right message
        LoginCustomer(db, "wronguser", "pass123")  # when user is wrong even if the password exist

def test_login_wrongPass(db):  # testing login function with no one with username
    AddCustomer(db, "testuser", "pass123", "Bella", "Kreit", "b@gmail.com", "818")
    with pytest.raises(ValueError, match="Incorrect password."):  # tests that the error is raised and it has right message
        LoginCustomer(db, "testuser", "wrongpassword")  # puts correct user but wrong password
