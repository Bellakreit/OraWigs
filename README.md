# 🪮 Ora Wigs

![Tests](https://img.shields.io/badge/tests-14%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-66%25-yellow)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/deployed-streamlit-ff4b4b)

A luxury wig e-commerce web app built with Streamlit. Browse wigs, compare prices, get AI-powered tutorials, and find the right hair color for your skin tone — all in one place.

🔗 **Live App:** [orawigs.streamlit.app](https://orawigs.streamlit.app/)

---

## 📋 Project Overview

Ora Wigs is a multi-page Streamlit application that combines web scraping, a SQLite3 database, data visualization, and AI integration to create an interactive wig shopping experience targeting the Jewish sheitel market.

### Features
- **Home Page** — New customer registration and existing customer login
- **Wig Popularity Page** — Interactive pie chart showing most popular wig types from purchase history
- **Compare Page** — Price comparison table between Ora Wigs and competitor prices scraped from shaniwigs.com
- **Order Page** — Custom wig order form that generates a pre-filled email
- **Tutorial Page** — AI chatbot (Mrs. Wigs) powered by Azure OpenAI to help customers learn about wigs and measure their heads
- **Hair Color Page** — Skin tone and hair color tips scraped from WikiHow and stored in the database

---

## 🗂 Project Structure

```
OraWigs/
├── OraWigs_app.py            # Main app entry point and navigation
├── Home.py                   # Customer registration and login
├── PopularWig.py             # Pie chart of popular wig types
├── Compare.py                # Price comparison table
├── HairColor.py              # Web scraping + hair color tips page
├── Tutorial.py               # AI chatbot page
├── Order.py                  # Custom order form
├── createDB.py               # Database setup and seeding
├── OraWigs.db                # SQLite3 database
├── tests/
│   ├── test_Home.py          # Tests for customer registration and login
│   ├── test_HairColor.py     # Tests for scraping and database
│   ├── test_Order.py         # Tests for order form logic
│   └── test_createDB.py      # Tests for API scraping and database
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Bellakreit/OraWigs.git
cd OraWigs
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up secrets
Create a file at `.streamlit/secrets.toml`:
```toml
AZURE_OPENAI_API_KEY = "your key here"
AZURE_OPENAI_ENDPOINT = "your endpoint here"
AZURE_OPENAI_MODEL = "your model name here"
```

### 5. Initialize the database
```bash
python createDB.py
```

### 6. Run the app
```bash
streamlit run OraWigs_app.py
```

---

## 🌐 Streamlit Cloud Deployment

The app is deployed on Streamlit Cloud and publicly accessible at [orawigs.streamlit.app](https://orawigs.streamlit.app/).

To deploy your own copy:
1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and select `OraWigs_app.py` as the main file
4. Add your secrets in **Settings → Secrets**

---

## 🕸 Web Scraping

Scraping is implemented in `HairColor.py` using `requests` and `BeautifulSoup`:
- Scrapes [wikihow.com/Choose-Hair-Color-for-Skin-Tone](https://www.wikihow.com/Choose-Hair-Color-for-Skin-Tone)
- Parses each step's heading and tip text using `div class="step"` and `<b>` tags
- Cleans citation markers like `[3]XResearch source` using regex
- Stores results in the `HairColorTips` table in SQLite3
- Clears old data before each re-scrape to prevent duplicates

---

## 🔌 API Data Retrieval

API data retrieval is implemented in `createDB.py`:
- Retrieves live product data from the Shani Wigs API at `shaniwigs.com/collections/wigs/products.json`
- Parses product tags and prices from the JSON response
- Pairs competitor prices with Ora Wigs prices and stores in the `ComparePrice` table
- Handles HTTP errors and invalid JSON responses with proper error handling

---

## 🗄 Database

SQLite3 database (`OraWigs.db`) with four tables:

| Table | Description |
|-------|-------------|
| `Customers` | Stores customer registration info |
| `Purchases` | Stores wig purchase history |
| `ComparePrice` | API retrieved competitor prices vs Ora prices |
| `HairColorTips` | Scraped hair color tips from WikiHow |

---

## 🤖 AI Integration

The **Tutorial Page** features Mrs. Wigs, an AI chatbot powered by **Azure OpenAI**.

- Uses the `AzureOpenAI` client from the `openai` Python library
- Streams responses in real time using `st.write_stream()`
- System prompt restricts Mrs. Wigs to only answer wig-related questions
- Maintains conversation history using `st.session_state`
- If the API is unavailable, a friendly error message is shown to the user
- API keys are stored securely in Streamlit Secrets Manager and never exposed in the repo

---

## 📊 Data Visualization

The **Wig Popularity Page** displays an interactive pie chart built with **Plotly Express** showing the distribution of wig types purchased, queried live from the `Purchases` table. The chart is interactive — users can hover over slices to see exact counts.

---

## 📦 Dependencies

```
streamlit
openai
pandas
plotly
requests
beautifulsoup4
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🧪 Testing

The test suite is in the `tests/` folder and covers database interactions, web scraping logic, business logic, and API calls via mocking.

### Run tests
```bash
pip install pytest pytest-cov
pytest tests/ -v
```

### Run with coverage report
```bash
pytest tests/ --cov=. --cov-report=term-missing
```

Coverage is measured using coverage.py via the pytest-cov plugin.

### Coverage Report
```
platform linux -- Python 3.11.13, pytest-9.0.3
14 passed in 1.74s

Name                      Stmts   Miss  Cover
---------------------------------------------
Compare.py                   10     10     0%
HairColor.py                 45      0   100%
Home.py                      70     37    47%
OraWigs_app.py               10     10     0%
Order.py                     32     20    38%
PopularWig.py                12     12     0%
Tutorial.py                  24     24     0%
createDB.py                  45     11    76%
---------------------------------------------
TOTAL                       364    124    66%
```

---

## 🔐 Environment Variables

Never commit your secrets to GitHub. Store them in `.streamlit/secrets.toml` locally and in Streamlit Cloud's Secrets Manager for deployment.

Required secrets:
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_MODEL`

Make sure `.streamlit/secrets.toml` is in your `.gitignore`.


