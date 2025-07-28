# ♻️ Earth911 Electronics Recycling Centers Scraper

This Python script scrapes recycling center data for **electronics disposal** near a given ZIP code from [Earth911](https://search.earth911.com/). The script uses an API proxy (Scrape.do) to render JavaScript-based content and extract details like **business name, address, and accepted materials**, exporting the cleaned results to a CSV file.

---

## 🚀 Features

- Extracts recycling center data dynamically from Earth911
- Handles JavaScript rendering using Scrape.do API
- Cleans messy HTML characters (e.g., ï»¿, â€”)
- Exports structured and readable CSV
- Handles missing data and scraping errors gracefully

---

## 🧰 Libraries & Tools Used

| Tool/Library       | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| `requests`         | For sending HTTP GET requests                                            |
| `urllib.parse`     | To safely encode the target URL                                          |
| `BeautifulSoup`    | HTML parsing and data extraction from the rendered response             |
| `pandas`           | Structuring and saving data to a CSV file                               |
| `unicodedata`      | Cleaning Unicode characters into plain ASCII                            |
| `Scrape.do API`    | Used to bypass JavaScript rendering and bot protection                  |

---

## 🧠 Scraping Logic

### 1. **Target URL**
We scrape from:
https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=100


This shows recycling centers accepting electronics in ZIP code `10001`.

---

### 2. **Handling JavaScript & Bot Protection**

Earth911 loads content dynamically, so we use [Scrape.do](https://scrape.do/) to render JavaScript and fetch fully loaded HTML.

✅ `render=true` ensures JS is loaded  
🔑 Requires an API key (`token=...`) for authentication

---

### 3. **Data Extraction using BeautifulSoup**

Each result item (`<li class="result-item">`) contains:

- **Business Name**
- **Street Address**
- **Accepted Materials**

We loop through all result cards and extract clean data into a dictionary.

---

### 4. **Data Cleaning**

Earth911 includes messy or non-ASCII characters (e.g., “ï»¿”, “â€””).

To clean this:

```python
import unicodedata

def clean_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    return text.strip()
