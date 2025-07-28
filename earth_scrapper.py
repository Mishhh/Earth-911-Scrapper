import requests
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
from html import unescape
import unicodedata


base_url = "https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=100"


encoded_url = urllib.parse.quote_plus(base_url)


api_key = "a9745136af2d4217a6b984674246d76b6602464fc32"
scrape_url = f"https://api.scrape.do/?url={encoded_url}&token={api_key}&render=true"


response = requests.get(scrape_url)


if response.status_code != 200:
    print(f"❌ Failed to fetch page, Status Code: {response.status_code}")
    exit()


soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.select('li.result-item')[:3]
print(f"🔎 Found {len(cards)} result items")


data = []
for card in cards:
    try:
        business_tag = card.select_one('h2.title a')
        business_name = business_tag.get_text(strip=True) if business_tag else "N/A"
        address = card.select_one('.contact .address3')
        address_text = address.get_text(strip=True) if address else "N/A"
        materials = card.select('.result-materials span.material')
        materials_list = [mat.get_text(strip=True) for mat in materials]
        materials_joined = ", ".join(materials_list)
        last_updated = "N/A"  

        
        data.append({
            "Business_name": business_name,
            "Last_update_date": last_updated,
            "Street_address": address_text,
            "Materials_accepted": materials_joined
        })
    except Exception as e:
        print(f"⚠️ Error parsing card: {e}")



def full_clean(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return text.strip()



df = pd.DataFrame(data)
df = df.applymap(full_clean)
df.to_csv("earth911_results.csv", index=False)
print("✅ Data saved to earth911_results.csv")
