import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# PostgreSQL Configuration
POSTGRES_URL = "postgresql://postgres:password@localhost:5432/aquarium_data"

# Create SQLAlchemy engine to connect to PostgreSQL
def get_engine():
    return create_engine(POSTGRES_URL)

# Load Data from PostgreSQL
def load_data():
    engine = get_engine()
    query = "SELECT * FROM sensor_readings"
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

# Streamlit Application
st.title("Aquarium Sensor Data Dashboard")

# Load data
st.write("Loading data from PostgreSQL...")
data = load_data()

# Data Overview
st.write("### Data Overview")
st.write(data.head(1000))

# Plot temperature over time
st.write("### Temperature Over Time")
temp_fig = px.line(data, x='timestamp', y='temperature', title='Temperature Over Time')
st.plotly_chart(temp_fig, key='temp_fig')

# Plot pH over time
st.write("### pH Level Over Time")
ph_fig = px.line(data, x='timestamp', y='ph', title='pH Level Over Time')
st.plotly_chart(ph_fig, key='ph_fig')

# Plot overall status counts
st.write("### Overall Status Counts")
status_counts = data['overall_status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
status_fig = px.bar(status_counts, x='Status', y='Count', title='Overall Status Counts')
st.plotly_chart(status_fig, key='status_fig')

# Custom Metric Selection for Visualization
st.write("### Custom Metric Visualization")
metric = st.selectbox("Select a metric to visualize:", ['temperature', 'tds', 'ph', 'nitrate', 'ammonia', 'nitrite', 'gh', 'kh'])
metric_fig = px.line(data, x='timestamp', y=metric, title=f'{metric.capitalize()} Over Time')
st.plotly_chart(metric_fig, key='metric_fig')

# Filter Alerts
st.write("### Filter Alerts")
alert_type = st.selectbox("Select an alert type:", ['temperature_alert', 'tds_alert', 'ph_alert', 'nitrate_alert', 'ammonia_alert', 'nitrite_alert', 'gh_alert', 'kh_alert'])
alert_data = data[data[alert_type] == 'ALERT']
st.write(f"### {alert_type.replace('_', ' ').capitalize()} Alerts")
st.write(alert_data)
