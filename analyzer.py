import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
import fredapi
import json
import os

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

FRED_API_KEY = "4f6e67caf7eb4f2e5f4d4946dd6b343e"

FOMC_URLS = [
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20240131.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20240320.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20240501.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20240612.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20240731.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20240918.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20241107.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomcminutes20241218.htm",
]

FOMC_DATES = [
    "2024-01-31", "2024-03-20", "2024-05-01", "2024-06-12",
    "2024-07-31", "2024-09-18", "2024-11-07", "2024-12-18"
]

HAWKISH = [
    "inflation", "tighten", "raise", "restrictive", "overheat",
    "aggressive", "elevated", "persistent", "above target",
    "strong", "robust", "resilient", "upside risk", "hike"
]

DOVISH = [
    "ease", "cut", "support", "accommodative", "slowdown",
    "unemployment", "cautious", "pause", "below target",
    "weak", "fragile", "downside risk", "reduce", "lower"
]

def fetch_fomc_text(url):
    try:
        headers = {"User-Agent": "Diya Shah diya.shah3108@rutgers.edu"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text.lower()
    except:
        return ""

def sentiment_score(text):
    if not text:
        return 0
    h = sum(text.count(w) for w in HAWKISH)
    d = sum(text.count(w) for w in DOVISH)
    return round((h - d) / (h + d + 1), 4)

def get_top_words(text, n=10):
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    stop = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in stop and len(t) > 3]
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]

print("Fetching FOMC transcripts...")
results = []
for i, url in enumerate(FOMC_URLS):
    print(f"  Fetching {FOMC_DATES[i]}...")
    text = fetch_fomc_text(url)
    score = sentiment_score(text)
    top_words = get_top_words(text)
    results.append({
        "date": FOMC_DATES[i],
        "sentiment": score,
        "top_words": top_words,
        "text_length": len(text)
    })

print("Fetching Fed Funds Rate from FRED...")
fred = fredapi.Fred(api_key=FRED_API_KEY)
fed_rate = fred.get_series("FEDFUNDS", observation_start="2024-01-01")
fed_df = pd.DataFrame({"date": fed_rate.index.strftime("%Y-%m-%d"), "fed_rate": fed_rate.values})

print("Saving data...")
with open("fomc_data.json", "w") as f:
    json.dump(results, f)

fed_df.to_csv("fed_rate.csv", index=False)
print("Done! Run: python3 -m streamlit run app.py")
