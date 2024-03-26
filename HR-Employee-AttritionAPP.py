import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv(r'C:\Users\Darshan\Downloads\HR-Employee-Attrition.csv')

def plot_attrition_by_education(filtered_df):
    education_levels = {
        1: 'Below College',
        2: 'College',
        3: 'Bachelor',
        4: 'Master',
        5: 'Doctor'
    }
    filtered_df['Education'] = filtered_df['Education'].map(education_levels)
    attrition_by_education = filtered_df.groupby('Education')['Attrition'].value_counts(normalize=True).unstack().fillna(0)
    if 'Yes' not in attrition_by_education.columns:
        attrition_by_education['Yes'] = 0  # Ensure 'Yes' column exists
    attrition_rates = attrition_by_education['Yes'] * 100
    fig, ax = plt.subplots()
    attrition_rates.plot(kind='bar', ax=ax)
    ax.set_xlabel('Education Level')
    ax.set_ylabel('Attrition Rate (%)')
    ax.set_xticklabels(attrition_rates.index, rotation=45)
    st.pyplot(fig)

def plot_age_distribution(filtered_df):
    fig, ax = plt.subplots()
    sns.histplot(data=filtered_df, x="Age", hue="Attrition", multiple="stack", kde=True, ax=ax)
    st.pyplot(fig)

def plot_overtime_effect(filtered_df):
    fig, ax = plt.subplots()
    sns.countplot(x="OverTime", hue="Attrition", data=filtered_df, ax=ax)
    st.pyplot(fig)

def plot_attrition_by_education_field(filtered_df):
    attrition_by_education = filtered_df.groupby(['EducationField', 'Attrition']).size().unstack(fill_value=0)
    fig, ax = plt.subplots()
    if 'Yes' in attrition_by_education.columns:
        attrition_by_education.plot(kind='pie', y='Yes', autopct='%1.1f%%', startangle=140, pctdistance=0.85, labels=attrition_by_education.index, ax=ax)
        ax.add_artist(plt.Circle((0,0),0.70,fc='white'))
    else:
        ax.text(0.5, 0.5, 'No Data Available', horizontalalignment='center', verticalalignment='center')
    ax.axis('equal')
    st.pyplot(fig)

def plot_attrition_by_job_role(filtered_df):
    attrition_by_jobrole = filtered_df.groupby(['JobRole', 'Attrition']).size().unstack(fill_value=0)
    fig, ax = plt.subplots()
    attrition_by_jobrole.plot(kind='barh', stacked=True, ax=ax)
    ax.set_xlabel('Number of Employees')
    ax.set_ylabel('Job Role')
    ax.legend(title='Attrition', labels=['No', 'Yes'])
    st.pyplot(fig)

# New plotting functions
def plot_attrition_counts(filtered_df):
    # Assuming 'filtered_df' is already filtered by the selected department
    attrition_counts = filtered_df['Attrition'].value_counts()
    plt.figure(figsize=(6, 4))
    attrition_counts.plot(kind='bar', color=['#2ca02c', '#d62728'])
    plt.title('Attrition Counts')
    plt.xlabel('Attrition')
    plt.ylabel('Count')
    plt.grid(axis='y')
    for i, count in enumerate(attrition_counts):
        plt.text(i, count, f' {count}', ha='center', va='bottom')
    st.pyplot(plt)

def plot_attrition_rate_by_years(filtered_df):
    # Assuming 'filtered_df' is already filtered by the selected department
    filtered_df['AttritionNumeric'] = filtered_df['Attrition'].map({'Yes': 1, 'No': 0})
    attrition_by_years = filtered_df.groupby('TotalWorkingYears')['AttritionNumeric'].mean().reset_index()
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=attrition_by_years, x='TotalWorkingYears', y='AttritionNumeric', marker='o')
    plt.title('Attrition Rate by Total Working Years')
    plt.xlabel('Total Working Years')
    plt.ylabel('Average Attrition Rate')
    st.pyplot(plt)

def plot_gender_counts(filtered_df):
    # Assuming 'filtered_df' is already filtered by the selected department
    gender_counts = filtered_df['Gender'].value_counts()
    plt.figure(figsize=(6, 4))
    gender_counts.plot(kind='bar', color=['#1f77b4', '#ff7f0e'])
    plt.title('Gender Counts')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.grid(axis='y')
    for i, count in enumerate(gender_counts):
        plt.text(i, count, f' {count}', ha='center', va='bottom')
    st.pyplot(plt)

# Function to display all graphs on one page
def display_all_graphs(department):
    st.title(f'{department} Department HR Attrition Dashboard')
    filtered_df = df[df['Department'] == department] if department != 'ALL' else df

    plot_attrition_counts(filtered_df)
    plot_attrition_rate_by_years(filtered_df)
    plot_gender_counts(filtered_df)
    # Add other plots as needed

# Main function to run the Streamlit app
def main():
    st.sidebar.title('Filter by Department')
    department_filter = st.sidebar.selectbox('Select Department', ['ALL'] + list(df['Department'].unique()))
    display_all_graphs(department=department_filter)

if __name__ == '__main__':
    main()
