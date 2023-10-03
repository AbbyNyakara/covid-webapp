# Import the libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import the data
# covid_data = pd.read_csv('michigan_vaccinations.csv')
# st.write(covid_data)

# Full view.
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Set the title
st.header("Michigan State Covid Vaccinations")

# Set the sidebar
with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")
