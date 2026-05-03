import pytest
import sqlite3
from unittest.mock import patch, Mock
import requests
from HairColor import createTable, scrapeAndStore, getInfo

# for me to test pytest tests/test_HairColor.py -v

@pytest.fixture
def db():  # making mock db for all tests
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

@pytest.fixture
def mock_response():  # making mock response to tests the methods
    mock = Mock()
    mock.raise_for_status.return_value = None
    # making mock response in correct format with div class="step" and the b tags like the wikihow page that is scraped
    mock.text = """
    <html><body>
        <div class="step"><b>Choose warm colors.</b>Warm tones look best with chestnut.</div>
        <div class="step"><b>Avoid cool colors.</b>Cool tones clash with warm skin.</div>
        <div class="step">No heading here.</div>
    </body></html>
    """
    return mock

def test_create_table(db):  # test the create table function to make sure the table exist after calling the function
    createTable(db)
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HairColorTips'")
    result = cur.fetchone()
    assert result is not None  # table should exist

@patch("requests.get")  # using patch to ignore the request in function and use mock instead
def test_scrape_and_store(mock_get, mock_response, db):
    mock_get.return_value = mock_response  # use fake response instead of real request
    createTable(db)
    scrapeAndStore(db)
    rows = getInfo(db)
    #test the functions and should return the two steps with these heading frommock response
    assert len(rows) == 2  # only 2 steps have headings, third one gets skipped
    assert rows[0][0] == "Choose warm colors."  # first heading
    assert rows[1][0] == "Avoid cool colors."  # second heading
    assert rows[1][1] == "Cool tones clash with warm skin." # second tip

@patch("requests.get")
def test_scrape_http_error(mock_get, db):  # tests it raises an error with bad http response
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
    createTable(db)
    scrapeAndStore(db)
    rows = getInfo(db)
    assert rows == []  # nothing should be inserted if request failed
