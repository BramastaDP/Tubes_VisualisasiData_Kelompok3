import streamlit as st
import pandas as pd
import altair as alt

# Set Streamlit page configuration
st.set_page_config(page_title="Top Universities Dashboard", layout="wide")

# Load dataset
@st.cache
def load_data():
    data = pd.read_csv("topuniversities.csv")
    data['Overall Score'] = pd.to_numeric(data['Overall Score'], errors='coerce')
    return data

data = load_data()

# App Title and Description
st.title("Top Universities Dashboard")
st.markdown("""
### Explore rankings, scores, and performance metrics of top universities worldwide.
This dashboard provides insights into various parameters, including academic reputation, research output, and international presence.
""")

# Sidebar Filters
st.sidebar.header("Filters")
country_filter = st.sidebar.multiselect("Select Countries:", data['Country'].unique(), default=data['Country'].unique())
metric_filter = st.sidebar.selectbox("Select Metric:", [
    "Overall Score", "Citations per Paper", "Papers per Faculty", 
    "Academic Reputation", "Faculty Student Ratio", "Staff with PhD",
    "International Research Center", "International Students", 
    "Employer Reputation", "Outbound Exchange", "Inbound Exchange"
])

filtered_data = data[data['Country'].isin(country_filter)]

# Key Metrics
st.header("Key Metrics")
top_university = filtered_data.iloc[0]['University Name']
highest_score = filtered_data.iloc[0]['Overall Score']
best_country = filtered_data.groupby("Country")['Overall Score'].mean().idxmax()
avg_best_score = filtered_data.groupby("Country")['Overall Score'].mean().max()

col1, col2, col3 = st.columns(3)
col1.metric("Top University", top_university)
col2.metric("Highest Overall Score", f"{highest_score:.2f}")
col3.metric("Best Country", f"{best_country} ({avg_best_score:.2f})")

# Distribution of Selected Metric
st.header(f"Distribution of {metric_filter}")
metric_chart = alt.Chart(filtered_data).mark_bar(opacity=0.85).encode(
    x=alt.X(f"{metric_filter}:Q", bin=alt.Bin(maxbins=20), title=f"{metric_filter}"),
    y=alt.Y('count()', title='Number of Universities'),
    color=alt.Color(f"{metric_filter}:Q", scale=alt.Scale(scheme='viridis')),
    tooltip=[alt.Tooltip(f"{metric_filter}:Q", title=f"{metric_filter}"), alt.Tooltip('count()', title='Count')]
).interactive().properties(
    title=f"Distribution of {metric_filter}",
    width=900,
    height=400
).configure_title(
    fontSize=18,
    anchor='start',
    color='gray'
)

st.altair_chart(metric_chart, use_container_width=True)

# Country-wise Average of Selected Metric
st.header(f"Average {metric_filter} by Country")
country_metric_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.Y("Country:N", sort='-x', title="Country"),
    y=alt.X(f"average({metric_filter}):Q", title=f"Average {metric_filter}"),
    color=alt.Color(f"average({metric_filter}):Q", scale=alt.Scale(scheme='turbo')),
    tooltip=[alt.Tooltip("Country:N", title="Country"), alt.Tooltip(f"average({metric_filter}):Q", title=f"Average {metric_filter}")]
).properties(
    title=f"Average {metric_filter} by Country",
    width=900,
    height=400
).configure_axis(
    labelAngle=0
).configure_title(
    fontSize=18,
    anchor='start',
    color='gray'
)

st.altair_chart(country_metric_chart, use_container_width=True)

# Detailed Data Table
st.header("Detailed University Data")
st.dataframe(filtered_data)

# Footer
st.markdown("Data source: Top Universities Dataset")