# Import required libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Title of the app
st.title("Survey Data Analysis")

# Data loading
@st.cache_data
def load_data():
    df = pd.read_csv('survey_data.csv')
    return df

df = load_data()

# Display the raw data
#if st.checkbox("Show raw data"):
    #st.write(df.head())

# Data cleaning
df = df.drop(['IP', 'Submission ID'], axis=1)

# Analysis: Top three countries represented in the dataset
country_counts = df['What country do you live in?'].value_counts()
top_countries = country_counts.head(5)

st.subheader("Top three countries represented in the dataset")
st.bar_chart(top_countries)

# Breakdown of respondents by profession in each of the top three countries
filtered_df = df[df['What country do you live in?'].isin(top_countries.index)]
profession_counts = filtered_df.groupby(['What country do you live in?', 'Are you a full-time professional papermaker, artist, paper/book conservator, or librarian, or are you engaged in other professions?']).size().unstack().fillna(0)

st.subheader("Breakdown of respondents by profession in top three countries")
st.bar_chart(profession_counts)

# Demographics analysis
demographics_columns = [
    'When did you first join NAHP/FDH/FDHPM?',
    'How would you describe your age:',
    'Have you ever participated in an NAHP exhibition?',
    'How often do you try to attend NAHP conferences?'
]

demographics_data = df[demographics_columns]
demographics_data.columns = ['Join_Date', 'Age', 'Participate_Exhibitions', 'Attend_Conferences']
demographics_data.dropna(subset=['Age', 'Participate_Exhibitions', 'Attend_Conferences'], inplace=True)

st.subheader("Demographics Summary")
st.write(demographics_data.describe(include='all'))

# Visualizations for Participation in exhibitions and Attendance at conferences
st.subheader("Participation in NAHP Exhibitions")
fig, ax = plt.subplots()
demographics_data['Participate_Exhibitions'].value_counts().plot(kind='bar', ax=ax)
st.pyplot(fig)

st.subheader("Attendance at NAHP Conferences")
fig, ax = plt.subplots()
demographics_data['Attend_Conferences'].value_counts().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Geographic Distribution - State (for US respondents)
geographic_distribution_state = df['If United States, please select your state:'].value_counts()

st.subheader("Geographic Distribution of Respondents by State (US)")
fig, ax = plt.subplots()
geographic_distribution_state.plot(kind='bar', ax=ax)
plt.title('Geographic Distribution of Respondents by State (US)')
plt.xlabel('State')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.grid(axis='y')
st.pyplot(fig)


