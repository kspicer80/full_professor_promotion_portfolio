import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import plotly.express as px

with open(r'downloaded_jsons\1158588_entries.json') as json_file:
    data = json.load(json_file)

extracted_data = []

for entry in data.values():
    for item in entry:
        extracted_data.append((item['user_id'], item['created_at'], item['message']))

df = pd.DataFrame(extracted_data, columns=['user_id', 'created_at', 'message'])
print(df.head())

def clean_text(text):
    import re
    text = re.sub(r'<.*?>', '', text) # remove HTML tags
    text = text.replace('\n', ' ').replace('&nbsp;', ' ')

    # replace Unicode characters
    text = text.translate(str.maketrans({'\u2019':"'"}))
    return text

df['message'] = df['message'].apply(clean_text)

def word_count(string):
    return len(string.split())

df['word_count'] = df['message'].apply(word_count)
print(df.head())

def read_in_and_count_words_in_posts(directory_path):
    list_for_dataframes = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith(".json"):
            # Load the JSON file
            with open(file_path) as infile:
                data = json.load(infile)

            canvas_course_id = os.path.splitext(os.path.basename(file_path))[0].split("_")[0]

        extracted_data = []

        for entry in data.values():
            for item in entry:
                extracted_data.append((item['user_id'], item['created_at'], item['message']))

            df = pd.DataFrame(extracted_data, columns=['user_id', 'created_at', 'message'])
            df['message'] = df['message'].apply(clean_text)
            df['word_count'] = df['message'].apply(word_count)
            df['canvas_course_id'] = canvas_course_id
            list_for_dataframes.append(df)
        full_dataframe = pd.concat(list_for_dataframes, ignore_index=True)

    return full_dataframe

path_to_json = r'G:\My Drive\DHStuff\projects\grad_courses_data_analysis\downloaded_jsons'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(json_files)

full_df = read_in_and_count_words_in_posts(path_to_json)
print(full_df.canvas_course_id.unique())
print(full_df.head())

grad_course_dictionary = {
    1170080: {'semester_year': 'Fall 2022', 'class_title': 'Composition Studies I, Theory'},
    1174400: {'semester_year': 'Spring 2023', 'class_title': 'Digital Rhetoric'},
    1170638: {'semester_year': 'Summer 2022', 'class_title': 'Digital Rhetoric'},
    1159984: {'semester_year': 'Summer 2021', 'class_title': 'Rhetorical Theory I, Classical'},
    1158588: {'semester_year': 'Spring 2021', 'class_title': 'Rhetorical Theory I, Classical'},
    1170054: {'semester_year': 'Summer 2022', 'class_title': 'Rhetorical Theory I, Classical'},
    1163662: {'semester_year': 'Fall 2021', 'class_title': 'Rhetorical Theory II, Contem'},
    1170078: {'semester_year': 'Fall 2022', 'class_title': 'Rhetorical Theory II, Contem'},
}

full_df['canvas_course_id'] = full_df['canvas_course_id'].astype(int)
full_df['semester_year'] = full_df['canvas_course_id'].map(lambda x: grad_course_dictionary[x]['semester_year'])
print(full_df.head())

print(full_df.groupby(['canvas_course_id', 'semester_year'])['word_count'].mean())

def plot_box_plots(df, course_id_column, word_count_column):
    fig, ax = plt.subplots()
    df.boxplot(column=word_count_column, by=course_id_column, ax=ax)
    ax.set_title("")
    labels = ['Spring 2021', 'Summer 2021', 'Fall 2021', 'Summer 2022', 'Fall 2022', 'Fall 2022', 'Summer 2022', 'Spring 2023']
    ax.set_xticklabels(labels)
    ax.set_ylabel("word_counts")
    plt.xticks(rotation=45)
    plt.show()

plot_box_plots(full_df, 'canvas_course_id', 'word_count')

def plot_stripplots(df, course_id_column, word_count_column):
    sns.stripplot(x=course_id_column, y=word_count_column, data= df, hue=course_id_column, jitter=.35, legend=False)
    plt.title('Word Count by Course ID')
    plt.xlabel('Course ID Number')
    plt.ylabel('Word Count')
    labels = ['Spring 2021', 'Summer 2021', 'Fall 2021', 'Summer 2022', 'Fall 2022', 'Fall 2022', 'Summer 2022', 'Spring 2023']
    plt.xticks(rotation=45)
    plt.xticks(df[course_id_column].unique(), labels, rotation=45)
    plt.show()

plot_stripplots(full_df, 'canvas_course_id', 'word_count')

full_df = full_df.sort_values(by=['created_at'])

fig = px.strip(full_df, x="word_count", y="canvas_course_id", color="canvas_course_id", hover_data=['created_at'], color_discrete_sequence=px.colors.qualitative.Vivid)

fig.update_layout(
    title_text='Word Count of Graduate Student Posts by Course ID',
    title_x=0.5,
    width=1400,
    height=500,
    yaxis=dict(title='Canvas Course ID'),
    xaxis=dict(title='Word Count')
)

fig.update_layout(showlegend=True)

fig.show()