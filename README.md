# MacroLens 🔭

An NLP-powered Federal Reserve policy sentiment analyzer that extracts hawkish and dovish signals from FOMC meeting transcripts and correlates them with real interest rate decisions.

## What it does
- Fetches and reads official Federal Reserve FOMC meeting transcripts
- Scores each meeting as hawkish, dovish, or neutral based on language signals
- Plots sentiment scores against actual Fed Funds Rate movements over time
- Shows top keywords driving the sentiment for each meeting

## Why it matters
Central banks communicate policy intentions through language before they act. This tool makes those signals visible and measurable, connecting NLP outputs to real macroeconomic outcomes.

## Tech Stack
Python, NLTK, BeautifulSoup, Plotly, Streamlit, FRED API, Federal Reserve FOMC Transcripts

## Run locally
pip install -r requirements.txt
python3 analyzer.py
streamlit run app.py

## Research Connection
This project extends my published SSRN research on monetary policy transmission and credit market behavior during contractionary cycles.
DOI: 10.2139/ssrn.5050841

## Author
Diya Shah — Rutgers University, BS Data Science & BA Economics# macrolens
