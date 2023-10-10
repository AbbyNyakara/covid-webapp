import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import numpy as np
# fig, ax = plt.subplots()

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
alt.data_transformers.enable('default', max_rows=6000)

st.header("Michigan State Covid Vaccinations")
st.markdown('''
    ### 1.0 Data
    - The data used is publicly available on [michigan.gov](https://www.michigan.gov/)
    - This has also been combined with the Michigan census data 
    ''')

# Load the data
df = pd.read_csv('michigan_vaccinations.csv')
st.write(df.head())

# Census Data
st.markdown('''
        **Statistics** - Source - [Census Data](https://www.census.gov/quickfacts/fact/table/MI/PST045222)
          - Total population: 10, 034, 113\n
            
          By Race: 
            - White/Caucasian: 78.8% / 7,906,881
            - Black/African-American: 14.1%/ 1,414,810
            - Asian/Native Hawaii/Pacific Island: 4% / 401, 365
            - Hispanic/Latino: 5.7% / 571, 944
            - Native Americans/Alaska Native: 0.7% / 70, 239
            -
        ''')

# Sidebar
with st.sidebar:
    st.write("Visualization settings")

# Add a select widget to the sidebar
chart_type1 = st.sidebar.selectbox(
    label='Chart 1 - Select the chart type:',
    options=['Bar Graph', 'Pie Chart']
)

# st.sidebar.write('Filter the race to view the Dose intakes')
# chart_type2 = st.sidebar.selectbox(
#     label='Chart 4 - Filter by Race/Ethnicity:',
#     options=['Select', 'Hispanic', 'NH White', 'NH Black',
#              'NH Asian/Native Hawaiian/Other Pacific Islands', 'NH American Indian/Alaska Native']
# )

######### End of sidebar #################

# chart 1 - Option 1
st.subheader('2.0 Data Exploration')
st.write('Chart 1 - Residents Vaccinated by age-group')

administered_doses = df.groupby(
    'Age Group')['Residents Vaccinated'].sum().reset_index()


if chart_type1 == 'Bar Graph':
    new_order = [9, 10, 5, 0, 1, 2, 3, 4, 6, 7, 8]
    administered_doses = administered_doses.iloc[new_order]
    residents_vaccinated = sns.barplot(x='Residents Vaccinated', y="Age Group",
                                       data=administered_doses, errwidth=0, palette="dark:#5A9_r")
    for i in residents_vaccinated.containers:
        residents_vaccinated.bar_label(i,)
    st.pyplot(residents_vaccinated.get_figure())
else:
    fig1 = px.pie(administered_doses, values='Residents Vaccinated', names='Age Group',
                  color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig1)

st.write("Considering Michigan's population for 60+ is about 19 percent of the total population(2million) they recorded higher vaccination rates ")


# Chart 2 - Vaccination Rates by Race.

st.subheader('Vaccinations by Race')
st.write('The graphs show the number of people vaccinated classified by race.')

administered_by_race = df.groupby(
    'Race/Ethnicity')['Residents Vaccinated'].sum().reset_index()

# Plot:
fig2 = px.pie(administered_by_race, values='Residents Vaccinated', names='Race/Ethnicity',
              color_discrete_sequence=px.colors.sequential.Plasma_r)
st.plotly_chart(fig2)

st.markdown('''
*of course this would make sense: considering the census statistics outlined at the beginning*
            
- A better comparison would be comparing the specific races against people vaccinated in that race. 
''')

# Chart 3.

st.subheader("Chart 3: Coverage by Race")

st.write('The chart displays the percentage of a certain ethnicity that got the vaccine. ')

df_dosage = df.groupby(['Race/Ethnicity', 'Dose']
                       )['Residents Vaccinated'].sum().reset_index()
df_dosage_grouped = df_dosage.groupby(
    'Race/Ethnicity')['Residents Vaccinated'].sum().reset_index()
df_dosage_grouped = df_dosage_grouped.assign(
    Population=[571944, 70238, 371262, 1414810, 7906881, 0])

# CHART 4
df_dosage_grouped['Percentage vaccinated'] = df_dosage_grouped['Residents Vaccinated'] / \
    df_dosage_grouped['Population'] * 100
df_dosage_grouped = df_dosage_grouped.drop(5)

# All vaccinated people 
plt.figure(figsize=(8, 6))
plt.title('Dose Coverage by Race')
plt4 = sns.barplot(df_dosage_grouped, x="Race/Ethnicity",
                   y="Percentage vaccinated", errorbar=None, color='pink')
plt4.bar_label(plt4.containers[0], fontsize=8)
plt4.set_xticklabels(plt4.get_xticklabels(),
                     rotation=20, ha="right", fontsize=8)
plt4.set_ylim(0, 100)
st.pyplot(plt4.get_figure())

st.write('The native asians/Native Hawaii population recorded the highest vaccination rates')
st.write("About 67.8% of The white and Hispanic population got the vaccine")
st.write('Only about 45.1% of the American Indian and 52.4% of the total black population in Michigan got the vaccine')


# Selection data


st.subheader('Chart 4 - Dosage coverage by Race/Ethnicity')

# Select the options
chart_type2  = st.selectbox(
    label='Chart 4 - Filter by Race/Ethnicity:',
    options=['Select', 'Hispanic', 'NH White', 'NH Black',
             'NH Asian/Native Hawaiian/Other Pacific Islands', 'NH American Indian/Alaska Native']
)

plt.title(f'Dosage coverage for {chart_type2}')
selected_df = df_dosage[df_dosage["Race/Ethnicity"] == f"{chart_type2}"]

fig3 = px.pie(selected_df, values='Residents Vaccinated', names='Dose',
             color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig3)

# Part 5
st.subheader('Chart 5- Explore/Create your own visualizations')

#List the counties
counties = df['County'].unique()

county_select  = st.selectbox(
    label = 'County:',
    options = np.insert(counties,0,'Select All')
)


