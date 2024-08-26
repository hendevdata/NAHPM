import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the logo
logo_path = 'ALL_NAHP_LOGO_V12D_HORIZONTAL_LOCKUP_OUTLINE.jpg'

def us_analysis():
    st.title("US Analysis")
    
    # Load the dataset
    df = pd.read_csv('survey_data.csv')
    
    # Show the first few rows
    st.write(df.head())

    # Removing columns that are not important to analyze
    df = df.drop(['IP', 'Submission ID'], axis=1)
    
    # Display the cleaned dataframe
    st.write(df.head())

    # --- Analysis 1: Top Three Countries by Respondents ---
    st.header("Top Three Countries by Respondents")
    country_counts = df['What country do you live in?'].value_counts()
    top_countries = country_counts.head(3)
    st.write(top_countries)

    # Plot the top three countries
    fig1, ax1 = plt.subplots()
    sns.barplot(x=top_countries.index, y=top_countries.values, ax=ax1)
    ax1.set_title('Top Three Countries by Number of Respondents')
    st.pyplot(fig1)

    # --- Analysis 2: Membership Levels ---
    st.header("Membership Levels Distribution")
    membership_levels = df['Please select your membership level:'].value_counts(3)
    st.write(membership_levels)

    # Plot the membership levels distribution
    fig2, ax2 = plt.subplots(figsize=(10, 6))  # Increase the figure size for better clarity
    sns.barplot(x=membership_levels.index, y=membership_levels.values, ax=ax2)


# Adjust title and label font sizes
    ax2.set_title('Membership Levels Distribution', fontsize=20)
    ax2.set_xlabel('Membership Level', fontsize=16)  # Increase x-axis label font size
    ax2.set_ylabel('Number of Respondents', fontsize=16)  # Increase y-axis label font size

# Adjust the font size of the tick labels
    ax2.tick_params(axis='x', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14)

# Rotate x labels for better readability and ensure they don't overlap
    plt.xticks(rotation=45, ha='right')

# Display the plot in Streamlit
    st.pyplot(fig2)

    # --- Analysis 3: Membership Changes ---
    st.header("Membership Changes Over Time")
    membership_changes = df['Over the last few years did you upgrade or downgrade your membership level to your current membership?'].value_counts()
    st.write(membership_changes)

    # Plot the membership changes
    fig3, ax3 = plt.subplots()
    sns.barplot(x=membership_changes.index, y=membership_changes.values, ax=ax3)
    ax3.set_title('Membership Changes Over Time')
    st.pyplot(fig3)

    # --- Analysis 4: Tenure by Membership Level ---
    st.header("Tenure by Membership Level")
    df['When did you first join NAHP/FDH/FDHPM?'] = pd.to_datetime(df['When did you first join NAHP/FDH/FDHPM?'], errors='coerce')
    df['Tenure (Years)'] = 2024 - df['When did you first join NAHP/FDH/FDHPM?'].dt.year
    tenure_by_level = df.groupby('Please select your membership level:')['Tenure (Years)'].mean()
    st.write(tenure_by_level)

    # Plot tenure by membership level
    fig, ax = plt.subplots(figsize=(10, 6))  # Increase the figure size for better clarity
    sns.barplot(x=tenure_by_level.index, y=tenure_by_level.values, ax=ax)
    ax.set_title('Average Tenure by Membership Level', fontsize=20)  # Increase title font size
    ax.set_xlabel('Membership Level', fontsize=1)  # Increase x-axis label font size
    ax.set_ylabel('Average Tenure (Years)', fontsize=10)  # Increase y-axis label font size
    
    # Rotate x labels for better readability and increase font size
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    st.pyplot(fig)


    # Additional analyses from the notebook can be added here similarly...

def non_us_analysis():
    st.title("Non-US Analysis")

    # Load the CSV file
    file_path = 'survey_data.csv'
    df = pd.read_csv(file_path)

    # Filter out non-US respondents based on the column 'What country do you live in?'
    non_us_country_df = df[df['What country do you live in?'] != 'United States']

    # Display the shape of the non-US data
    st.write(f"Number of non-US respondents: {non_us_country_df.shape[0]}")

    # --- Analysis 1: Country Distribution ---
    st.header("Country Distribution")
    country_distribution = non_us_country_df['What country do you live in?'].value_counts()
    st.write(country_distribution)
    
    # Plotting the country distribution with a pie chart
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    ax1.pie(country_distribution, labels=country_distribution.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=140)
    ax1.axis('equal')
    st.pyplot(fig1)

    # --- Analysis 2: Membership Levels by Country ---
    st.header("Membership Levels by Country")
    membership_by_country = non_us_country_df.groupby('What country do you live in?')['Please select your membership level:'].value_counts().unstack()
    st.write(membership_by_country)
    
    # Plotting the membership levels by country
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    membership_by_country.plot(kind='bar', stacked=True, ax=ax2, color=plt.cm.Paired.colors)
    st.pyplot(fig2)

    # --- Analysis 3: Membership Tenure by Country ---
    st.header("Membership Tenure by Country")
    non_us_country_df['When did you first join NAHP/FDH/FDHPM?'] = pd.to_datetime(non_us_country_df['When did you first join NAHP/FDH/FDHPM?'], errors='coerce')
    non_us_country_df = non_us_country_df.dropna(subset=['When did you first join NAHP/FDH/FDHPM?'])
    non_us_country_df['Tenure (Years)'] = 2024 - non_us_country_df['When did you first join NAHP/FDH/FDHPM?'].dt.year
    average_tenure_by_country = non_us_country_df.groupby('What country do you live in?')['Tenure (Years)'].mean()
    st.write(average_tenure_by_country)
    
    # Plotting average tenure by country
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    average_tenure_by_country.plot(kind='bar', color='lightblue', ax=ax3)
    st.pyplot(fig3)

    # --- Analysis 4: Tenure's Effect on Upgrades ---
    st.header("Effect of Membership Tenure on Upgrades/Downgrades")
    tenure_vs_upgrade = non_us_country_df[['Tenure (Years)', 'Over the last few years did you upgrade or downgrade your membership level to your current membership?']]
    tenure_effect_on_upgrade = tenure_vs_upgrade.groupby('Over the last few years did you upgrade or downgrade your membership level to your current membership?')['Tenure (Years)'].mean()
    st.write(tenure_effect_on_upgrade)
    
    # Plotting the effect of tenure on upgrades/downgrades
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    tenure_effect_on_upgrade.plot(kind='bar', color='orange', ax=ax4)
    st.pyplot(fig4)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["US Analysis", "Non-US Analysis"])

if page == "US Analysis":
    us_analysis()
elif page == "Non-US Analysis":
    non_us_analysis()
