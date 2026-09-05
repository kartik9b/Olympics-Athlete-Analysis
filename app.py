import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Olympic Analytics Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished metric styling
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CACHED DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("athlete_data.csv")
    df['Medal'] = df['Medal'].fillna("No Medal")
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. INTERACTIVE SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.title("🏅 Filters")

# Filter 1: Season
seasons = ["All"] + list(df["Season"].unique())
selected_season = st.sidebar.selectbox("Select Season", seasons)

# Filter 2: Year Range Slider
min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (1980, max_year))

# Filter 3: Sport Dropdown
sports = ["All"] + sorted(list(df["Sport"].unique()))
selected_sport = st.sidebar.selectbox("Select Sport", sports)

# Apply Filter Transformations
filtered_df = df.copy()

if selected_season != "All":
    filtered_df = filtered_df[filtered_df["Season"] == selected_season]

filtered_df = filtered_df[
    (filtered_df["Year"] >= selected_years[0]) & 
    (filtered_df["Year"] <= selected_years[1])
]

if selected_sport != "All":
    filtered_df = filtered_df[filtered_df["Sport"] == selected_sport]

# -----------------------------------------------------------------------------
# 4. DASHBOARD HEADER & KPIS
# -----------------------------------------------------------------------------
st.markdown("<h1 class='main-title'>Olympic History & Performance Analytics</h1>", unsafe_allow_html=True)
st.caption(f"Analyzing **{selected_years[0]} - {selected_years[1]}** | Filtered Entries: **{len(filtered_df):,}**")

st.markdown("---")

# Render KPI Columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Unique Athletes", value=f"{filtered_df['ID'].nunique():,}")

with col2:
    st.metric(label="Nations (NOCs)", value=f"{filtered_df['NOC'].nunique():,}")

with col3:
    medals_awarded = len(filtered_df[filtered_df['Medal'] != 'No Medal'])
    st.metric(label="Total Medals Awarded", value=f"{medals_awarded:,}")

with col4:
    female_pct = (filtered_df['Sex'].value_counts(normalize=True).get('F', 0)) * 100
    st.metric(label="Female Ratio", value=f"{female_pct:.1f}%")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. TABBED PLOTLY VISUALIZATIONS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Participation Trends", "🏆 Medal Standings", "📊 Physical Attributes"])

# TAB 1: Line Chart (Participation)
with tab1:
    st.subheader("Athlete Participation Over Time")
    gender_trend = filtered_df.groupby(['Year', 'Sex'])['ID'].nunique().reset_index()
    
    fig_trend = px.line(
        gender_trend, 
        x="Year", 
        y="ID", 
        color="Sex",
        labels={"ID": "Athletes", "Sex": "Gender"},
        color_discrete_map={"M": "#2563EB", "F": "#EC4899"},
        markers=True
    )
    fig_trend.update_layout(template="plotly_white", hovermode="x unified", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_trend, use_container_width=True)

# TAB 2: Stacked Bar Chart (Medals)
with tab2:
    st.subheader("Top 10 Medal-Winning Nations")
    
    medal_df = filtered_df[filtered_df['Medal'] != 'No Medal']
    if not medal_df.empty:
        top_10_nocs = medal_df['NOC'].value_counts().head(10).index
        top_nocs_df = medal_df[medal_df['NOC'].isin(top_10_nocs)].groupby(['NOC', 'Medal'])['ID'].count().reset_index(name='Count')
        
        fig_bar = px.bar(
            top_nocs_df,
            x="NOC",
            y="Count",
            color="Medal",
            color_discrete_map={"Gold": "#EAB308", "Silver": "#94A3B8", "Bronze": "#B45309"},
            category_orders={"Medal": ["Gold", "Silver", "Bronze"]},
            barmode="stack"
        )
        fig_bar.update_layout(template="plotly_white", xaxis_title="Country NOC", yaxis_title="Total Medals")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No medal data available for the selected filters.")

# TAB 3: Interactive Scatter Plot
with tab3:
    st.subheader("Height vs. Weight Distribution")
    
    clean_physical = filtered_df.dropna(subset=['Height', 'Weight'])
    if not clean_physical.empty:
        sample_size = min(2500, len(clean_physical))
        sample_df = clean_physical.sample(sample_size, random_state=42)
        
        fig_scatter = px.scatter(
            sample_df,
            x="Height",
            y="Weight",
            color="Sex",
            hover_data=["Name", "Sport", "Medal"],
            opacity=0.6,
            color_discrete_map={"M": "#2563EB", "F": "#EC4899"},
            labels={"Height": "Height (cm)", "Weight": "Weight (kg)"}
        )
        fig_scatter.update_layout(template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No physical attribute data available for these filters.")

# -----------------------------------------------------------------------------
# 6. EXPANDABLE DATA TABLE INSPECTOR
# -----------------------------------------------------------------------------
with st.expander("🔍 Inspect Filtered Dataset"):
    st.dataframe(
        filtered_df[["Name", "Sex", "Age", "Team", "NOC", "Games", "Sport", "Event", "Medal"]].head(200),
        use_container_width=True
    )