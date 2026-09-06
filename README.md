# Olympics-Athlete-Analysis

# 🏅 Olympic History & Performance Analytics Dashboard

An interactive, data-driven Streamlit web application designed to analyze over a century of Olympic Games data. This dashboard allows users to explore athlete participation trends, country-level medal tallies, and physical attributes across various sports and eras.

---

## 🚀 Features

- **Interactive Filtering:** Filter data dynamically by Season (Summer/Winter), Year Range, and specific Sports.
- **Key Performance Indicators (KPIs):** Instant summary metrics showing total unique athletes, participating nations (NOCs), total medals awarded, and gender ratio.
- **Participation Trends:** Visual representation of athlete participation over time segmented by gender using Plotly line charts.
- **Medal Standings:** Stacked bar charts displaying top medal-winning nations breakdown (Gold, Silver, Bronze).
- **Physical Attribute Insights:** Scatter plot analysis comparing athlete height vs. weight distributions across genders and sports.
- **Raw Data Inspector:** Expandable dataset viewer to inspect granular athlete records.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **Data Visualization:** [Plotly Express](https://plotly.com/python/plotly-express/)
- **Storage Optimization:** Apache Arrow / Parquet

---

## 📁 Repository Structure

```text
├── app.py                      # Main Streamlit application file
├── athlete_data.parquet        # Processed Olympic dataset (Parquet format)
├── requirements.txt            # Python dependencies for deployment
└── README.md                   # Project documentation
