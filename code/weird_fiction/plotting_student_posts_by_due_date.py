import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sqlalchemy import create_engine
import seaborn as sns

# Connect to the PostgreSQL database using SQLAlchemy
engine = create_engine('postgresql://spicy.kev:@localhost:5432/weird_fiction')

query = """
SELECT mp.discussion_topic_id, mp.canvas_course_id, mp.created_at, add.due_at,
       mp.created_at - add.due_at AS days_difference
FROM main_posts mp
JOIN discussion_board_assignment_data dbad ON mp.discussion_topic_id = dbad.discussion_topic_id AND mp.canvas_course_id = dbad.canvas_course_id
JOIN assignment_due_dates add ON dbad.assignment_id = add.assignment_id
"""

df = pd.read_sql(query, engine)
print(df.head())

# Convert 'created_at' and 'due_at' columns to datetime type
df['created_at'] = pd.to_datetime(df['created_at'])
df['due_at'] = pd.to_datetime(df['due_at'], utc=True)

# Get unique course_ids
unique_course_ids = df['canvas_course_id'].unique()

# Set the number of rows and columns for the subplots grid
num_rows = 2  # Adjust the number of rows as desired
num_cols = 5  # Adjust the number of columns as desired
num_subplots = num_rows * num_cols

# Create the subplots grid
fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 8))

# Flatten the axes array to simplify indexing in the loop
axes = axes.flatten()

# Iterate over each unique course_id and plot the corresponding data
for i, course_id in enumerate(unique_course_ids[:num_subplots]):
    # Filter the DataFrame for the current course_id
    subset_df = df[df['canvas_course_id'] == course_id]

    # Set the style of the plot
    sns.set_style("whitegrid", {"axes.facecolor": "0.9"})

    # Create the scatter plot with jitter and color-coded by 'course_id'
    jitter_range = pd.Timedelta(days=0.5)  # Adjust the jitter range as needed
    opacity = 0.5  # Set the opacity value (0.0 to 1.0)
    sns.stripplot(data=subset_df, x='created_at', y=None, alpha=opacity, jitter=True, hue='canvas_course_id', ax=axes[i])

    # Get unique due dates and their corresponding counts
    unique_due_dates = subset_df['due_at'].unique()
    counts = subset_df['due_at'].value_counts()

    # Set the x-axis tick marks to the unique due dates
    axes[i].set_xticks(ticks=unique_due_dates)
    axes[i].tick_params(axis='x', rotation=90)

    # Loop through each unique due date and plot a vertical line
    for due_date in unique_due_dates:
        count = counts[due_date]
        axes[i].axvline(x=due_date, ymin=0, ymax=count, color='red', linestyle='--')

    # Remove y-axis ticks and labels
    axes[i].set_yticks([])

    # Set the title of the subplot
    axes[i].set_title(f'Course ID: {course_id}')

# Remove any empty subplots
if num_subplots < len(unique_course_ids):
    for j in range(num_subplots, len(unique_course_ids)):
        fig.delaxes(axes[j])

# Set the labels and title of the overall plot
fig.text(0.5, 0.04, 'Post Creation Date', ha='center')
fig.suptitle('Post Creation Dates vs Due Dates (Color-coded by Course ID)', y=0.92)

# Adjust the spacing between subplots
fig.tight_layout(pad=2.0)

# Display the plot
plt.show()
plt.savefig('due_dates.png')
