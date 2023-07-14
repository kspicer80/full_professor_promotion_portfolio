import pandas as pd
import os
import matplotlib.pyplot as plt

# Path to the folder containing Excel files
folder_path = r"C:\Users\KSpicer\Desktop\grad_course_enrollments"

# Initialize an empty DataFrame
dfs = []

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):  # Check if it's an Excel file
        file_path = os.path.join(folder_path, filename)

        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Extract the file name without extension
        file_name = os.path.splitext(filename)[0]

        # Add a new column with the file name
        df['file_name'] = file_name

        # Append the current DataFrame to the combined DataFrame
        dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# Display the combined DataFrame
print(combined_df.head())

semester_year_dict = {
    'f_2020': 'Fall 2020',
    'f_2021': 'Fall 2021',
    'f_2022': 'Fall 2022',
    'spring_2021': 'Spring 2021',
    'spring_2022': 'Spring 2022',
    'spring_2023': 'Spring 2023',
    'summer_2021': 'Summer 2021',
    'summer_2022': 'Summer 2022',
    'summer_2023': 'Summer 2023'
}

combined_df['file_name'] = combined_df['file_name'].map(semester_year_dict)
combined_df = combined_df.rename(columns={'file_name': 'semester_year'})
print(combined_df.head())
#combined_df = combined_df[combined_df['Total Seats'] != 0]

desired_order = ['Fall 2020', 'Spring 2021', 'Summer 2021', 'Fall 2021', 'Spring 2022', 'Summer 2022', 'Fall 2022', 'Summer 2023', 'Spring 2023']
grouped = combined_df.groupby(['semester_year'])['Enrolled'].sum()
grouped_sorted = grouped.loc[desired_order]

ax = grouped_sorted.plot(kind='bar', color='magenta')
plt.xlabel('Semester/Year')
plt.ylabel('Number of Enrolled Students')
plt.title('ENGE/ENGM Course Enrollments Over Time')

#for i, v in enumerate(grouped_sorted):
    #ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')
plt.show()