# 🛍️ Myntra Review Scraper

A full-stack web scraper that extracts and analyzes customer reviews from [Myntra](https://www.myntra.com/) — India's leading fashion e-commerce platform. Built with **Selenium**, **Streamlit**, and **MongoDB**, it provides interactive dashboards with **Plotly** visualizations for review sentiment analysis.

---

## ✨ Features

- 🔍 **Product Search** — Search any product on Myntra by name
- 🤖 **Automated Scraping** — Selenium-powered browser automation extracts reviews, ratings, prices, and user details
- 💾 **Cloud Storage** — Scraped data stored in MongoDB Atlas for persistence
- 📊 **Interactive Dashboard** — Plotly-based analytics with pie charts, bar graphs, and review breakdowns
- 📄 **CSV Export** — Auto-saves scraped data to `data.csv` for offline analysis
- 🌐 **Dual Frontend** — Streamlit (recommended) + Flask web interfaces

---

## 🏗️ Architecture

```
User Input (Product + Count)
        │
        ▼
┌──────────────────┐
│  Selenium Chrome │──── Navigates Myntra ────▶ Product Pages
│  + BeautifulSoup │──── Parses HTML ─────────▶ Reviews Data
└──────────────────┘
        │
        ▼
┌──────────────────┐     ┌──────────────┐
│  Pandas DataFrame│────▶│  MongoDB     │
│                  │     │  Atlas       │
│                  │────▶│  data.csv    │
└──────────────────┘     └──────────────┘
        │
        ▼
┌──────────────────┐
│  Streamlit UI    │
│  + Plotly Charts │──── Interactive Dashboard
└──────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10** | Core language |
| **Selenium** | Browser automation for web scraping |
| **BeautifulSoup4** | HTML parsing |
| **Streamlit** | Interactive web UI and dashboard |
| **Flask** | Alternative lightweight web UI |
| **Plotly** | Interactive charts and visualizations |
| **MongoDB Atlas** | Cloud database for storing reviews |
| **Pandas** | Data manipulation and analysis |

---

## 📁 Project Structure

```
Myntra_Scraper/
├── app.py                    # Streamlit app (main entry point)
├── application.py            # Flask app (alternative entry point)
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── .env                      # MongoDB connection string (not in repo)
│
├── src/
│   ├── scrapper/
│   │   └── scrape.py         # Core scraping logic (Selenium + BS4)
│   ├── cloud_io/
│   │   └── __init__.py       # MongoDB read/write operations
│   ├── data_report/
│   │   └── generate_data_report.py  # Plotly dashboard generator
│   ├── constants/
│   │   └── __init__.py       # Configuration constants
│   ├── utils/
│   │   └── __init__.py       # Helper utilities
│   └── exception.py          # Custom exception handling
│
├── pages/
│   └── generate_analysis.py  # Streamlit analytics page
│
├── templates/                # Flask HTML templates
│   ├── base.html
│   ├── index.html
│   └── results.html
│
└── static/css/               # Stylesheets for Flask UI
    ├── style.css
    └── main.css
```

---

## 🚀 How to Setup & Run

### Prerequisites

- **Python 3.10+**
- **Google Chrome** browser installed
- **MongoDB Atlas** account ([free tier](https://www.mongodb.com/atlas))

### Step 1 — Clone the repository

```bash
git clone https://github.com/Yash13Agrawal/Myntra-Review-Scraper.git
cd Myntra-Review-Scraper/Myntra_Scraper
```

### Step 2 — Create a virtual environment

```bash
python -m venv env

# Activate (Windows)
.\env\Scripts\Activate.ps1

# Activate (Mac/Linux)
source env/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you get a ChromeDriver version mismatch, update `chromedriver-binary` version in `requirements.txt` to match your Chrome browser version.

### Step 4 — Configure MongoDB

1. Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a database user and whitelist your IP
3. Get your connection string
4. Create a `.env` file in the project root:

```env
MONGO_DB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
```

### Step 5 — Run the application

**Streamlit (Recommended):**
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

**Flask (Alternative):**
```bash
python application.py
```
Open `http://127.0.0.1:8000` in your browser.

---

## 📊 Dashboard Features

The analytics dashboard (Streamlit sidebar → "generate_analysis") provides:

| Chart | Description |
|---|---|
| 🥧 **Pie Chart** | Average ratings distribution by product |
| 📊 **Bar Chart** | Price comparison across products |
| ✨ **Positive Reviews** | Top reviews with rating ≥ 4.5 |
| 💢 **Negative Reviews** | Reviews with rating ≤ 2 |
| 🔹 **Rating Counts** | Distribution of ratings per product |

---

## 📝 How It Works

1. **Search** — Enter a product name (e.g., "sunscreen") and the number of products to scrape
2. **Scrape** — Selenium opens Chrome, searches Myntra, visits each product page, and scrolls through reviews
3. **Parse** — BeautifulSoup extracts review text, rating, reviewer name, date, product price, and overall rating
4. **Store** — Data is saved to MongoDB Atlas and exported as `data.csv`
5. **Analyze** — Navigate to the analytics page for interactive Plotly charts and review insights

---

## ⚠️ Important Notes

- Selenium opens a **visible Chrome window** during scraping — don't interact with it while scraping is in progress
- Myntra may update their HTML structure, which could break CSS selectors in the scraper
- The `.env` file containing MongoDB credentials is excluded from version control via `.gitignore`
- The `data.csv` file is also excluded from the repo

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👤 Author

**Yash Agrawal**
- GitHub: [@Yash13Agrawal](https://github.com/Yash13Agrawal)

---

⭐ If you found this project helpful, please give it a star!