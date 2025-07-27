import streamlit as st
import pandas as pd
from queries import queries
from db_connection import get_connection

# Set up Streamlit layout and title
st.set_page_config(layout="wide", page_title="Nutrition Paradox Dashboard")
st.title("🍽 Nutrition Paradox: Global Obesity & Malnutrition Dashboard")

# Sidebar: Query selection
st.sidebar.header("🔍 Query Explorer")
query_name = st.sidebar.selectbox("Select Analysis", list(queries.keys()))

# Get database connection
conn = get_connection()

# Display selected query title
st.subheader(query_name)

try:
    sql = queries[query_name]

    # Handle multiple queries separated by semicolon
    for individual_sql in sql.strip().split(';'):
        individual_sql = individual_sql.strip()
        if individual_sql:
            # Run query and display result
            df = pd.read_sql_query(individual_sql, conn)

            # Scrollable DataFrame display
            st.dataframe(df, height=400)

            # Optional: Print columns present
            # st.write(df.columns)

            # Auto-plot for time series or region-based data
            if not df.empty:
                if 'Year' in df.columns and df.select_dtypes(include='number').shape[1] >= 2:
                    for col in df.columns:
                        if col != 'Year':
                            st.line_chart(df.set_index('Year')[col])
                elif 'Country' in df.columns and df.select_dtypes(include='number').shape[1] >= 1:
                    st.bar_chart(df.set_index('Country'))
except Exception as e:
    st.error(f"❌ Failed to execute query: {e}")

# Footer
st.caption("""This dashboard was built to explore the dual burden of malnutrition and obesity using WHO datasets. © 2025""")