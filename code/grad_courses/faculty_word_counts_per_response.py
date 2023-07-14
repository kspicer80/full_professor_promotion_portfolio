import json
import requests
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

API_KEY = 'Your Canvas API Key Goes Here'
header_argument = {"Authorization": "Bearer " + API_KEY}

def get_all_pages(url):
    data = []
    while url:
        response = requests.get(url, headers=header_argument)
        data.extend(response.json())
        link_header = response.headers.get("Link")
        if link_header:
            url = next_url_from_link_header(link_header)
        else:
            url = None
    return data

def next_url_from_link_header(link_header):
    for link in link_header.split(","):
        if "rel=\"next\"" in link:
            return link.split(";")[0][1:-1]
    return None

grad_course_dictionary = [
    {'canvas_course_id': 1170080, 'semester_year': 'Fall 2022', 'class_title': 'Composition Studies I, Theory'},
    {'canvas_course_id': 1174400, 'semester_year': 'Spring 2023', 'class_title': 'Digital Rhetoric'},
    {'canvas_course_id': 1170638, 'semester_year': 'Summer 2022', 'class_title': 'Digital Rhetoric'},
    {'canvas_course_id': 1159984, 'semester_year': 'Summer 2021', 'class_title': 'Rhetorical Theory I, Classical'},
    {'canvas_course_id': 1158588, 'semester_year': 'Spring 2021', 'class_title': 'Rhetorical Theory I, Classical'},
    {'canvas_course_id': 1170054, 'semester_year': 'Summer 2022', 'class_title': 'Rhetorical Theory I, Classical'},
    {'canvas_course_id': 1163662, 'semester_year': 'Fall 2021', 'class_title': 'Rhetorical Theory II, Contem'},
    {'canvas_course_id': 1170078, 'semester_year': 'Fall 2022', 'class_title': 'Rhetorical Theory II, Contem'}
]
## First Step: Grab all the Assignment ID numbers:
course_number_list = [course['canvas_course_id'] for course in grad_course_dictionary]
course_number_list

all_data_together = list()

for course_number in course_number_list:
    url = f'https://stfrancis.instructure.com:443/api/v1/courses/{course_number}/assignments?include[]=submission'
    data = get_all_pages(url)
    all_data_together.append(data)

json.dump(all_data_together, open('all_data_together.json', 'w'), indent=4)
## Second Step: Grab all the Submission Comments for Each Assignment ID:
with open('all_data_together.json') as json_file:
    json_data = json.load(json_file)

course_id_and_assignment_ids = []

for course in json_data:
    for assignment in course:
        course_id_and_assignment_ids.append((assignment['course_id'], assignment['id']))
course_id_and_assignment_ids[0]
len(course_id_and_assignment_ids)
all_submission_data = []

for item in course_id_and_assignment_ids:
    api_request_url = f'https://stfrancis.instructure.com:443/api/v1/courses/{item[0]}/assignments/{item[1]}/submissions?include[]=submission_comments'
    submission_comment_data = get_all_pages(api_request_url)
    all_submission_data.append(submission_comment_data)

json.dump(all_submission_data, open('all_submission_data.json', 'w'), indent=4)

def flatten_json(json_data, prefix=''):
    flattened = {}
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            flattened.update(flatten_json(value, new_key))
    elif isinstance(json_data, list):
        for index, item in enumerate(json_data):
            new_key = f"{prefix}[{index}]"
            flattened.update(flatten_json(item, new_key))
    else:
        flattened[prefix] = json_data
    return flattened

with open('all_submission_data.json') as json_file:
    json_data = json.load(json_file)

flattened_data = flatten_json(json_data)
json.dump(flattened_data, open('flattened_data.json', 'w'), indent=4)

def extract_value_by_key(json_data, key):
    values = []
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                values.append(v)
            elif isinstance(v, (dict, list)):
                values.extend(extract_value_by_key(v, key))
    elif isinstance(json_data, list):
        for item in json_data:
            values.extend(extract_value_by_key(item, key))
    return values

submission_comments = extract_value_by_key(json_data, 'submission_comments')
submission_comments[0]
print(len(submission_comments))
len(json_data)
second_level_json_data = []

for item in json_data:
    second_level_json_data.append(item)
second_level_json_data[0]
submission_comments_extracted = []

for item in second_level_json_data:
    for sublist in item:
        for key, value in sublist.items():
            if key == 'submissions_comment':
                submission_comments_extracted.append('value')
            else:
                continue

len(submission_comments_extracted)
submission_comments[1]
len(submission_comments)
submission_comments[0]
submission_comments[26]

with open('filtered_submission_comments.json', 'w') as json_file:
    json.dump(submission_comments, json_file, indent=4)
if "submissions_comment" in submission_comments:
    # Extract the list of dictionaries under the key "submission_comments"
    submission_comments = submission_comments["submission_comments"]
    # Set the specific author_id to filter by
    target_author_id = 'Your Canvas ID goes here ...'

    # Filter comments by author_id
    filtered_comments = [comment for comment in submission_comments if "author_id" in comment and comment["author_id"] == target_author_id]

    # Print the filtered comments
    for comment in filtered_comments:
        print(comment)
else:
    print("No submission comments found.")
import json

def extract_value_by_key(json_data, key):
    values = []
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                values.append(v)
            elif isinstance(v, (dict, list)):
                values.extend(extract_value_by_key(v, key))
    elif isinstance(json_data, list):
        for item in json_data:
            values.extend(extract_value_by_key(item, key))
            if isinstance(item, list):
                for sub_item in item:
                    values.extend(extract_value_by_key(sub_item, key))
    return values

# Load the JSON data from file
with open('all_submission_data.json', 'r') as file:
    json_data = json.load(file)

# Extract the values for the key "submission_comments"
submission_comments = extract_value_by_key(json_data, "submission_comments")

# Set the specific author_id to filter by
target_author_id = 'Your Canvas ID goes here ...'

# Filter comments by author_id
filtered_comments = [comment for comment_list in submission_comments for comment in comment_list if isinstance(comment, dict) and "author_id" in comment and comment["author_id"] == target_author_id]

# Print the filtered comments
#for comment in filtered_comments:
    #print(comment)

with open('filtered_submission_comments.json', 'w') as json_file:
    json.dump(filtered_comments, json_file, indent=4)
import unicodedata
import re

with open("prep_data_cleaning/filtered_submission_comments.json", "r") as file:
    filtered_comments = json.load(file)

for comment in filtered_comments:
    comment["comment"] = unicodedata.normalize("NFKD", comment["comment"]).encode("ascii", "ignore").decode("utf-8")
    words = comment["comment"].split()
    comment["word_count"] = len(words)
    html_url = comment["author"]["html_url"]
    course_id = re.search(r'/courses/(\d+)/users/', html_url)
    if course_id:
        comment["course_id"] = course_id.group(1)

with open("filtered_submission_comments_unicode_cleaned.json", "w") as file:
    json.dump(filtered_comments, file, indent=4)


df = pd.read_json("filtered_submission_comments_unicode_cleaned.json")
df.head()
df = df.drop(columns=['edited_at', 'attempt', 'avatar_path', 'author', 'attachments'])
df.head()
average_submission_response_length = df['word_count'].mean()
average_submission_response_length
total_words_written_in_response = df['word_count'].sum()
total_words_written_in_response
grouped_by_course_df = df.groupby('course_id')['word_count'].mean()
grouped_by_course_df.plot(kind='bar')
## Now let's just get the number of users per course ...:
course_number_and_total_student_count_dict = dict()

for course_number in course_number_list:
    url = f'https://stfrancis.instructure.com:443/api/v1/courses/{course_number}/users?enrollment_type[]=student'
    data = get_all_pages(url)
    course_number_and_total_student_count_dict[course_number] = len(data)
course_number_and_total_student_count_dict


course_id_dict = {course['canvas_course_id']: course['semester_year'] for course in grad_course_dictionary}

ax = grouped_by_course_df.plot(kind='bar', color='orange')

ax.set_xticklabels([course_id_dict.get(course_id, '') for course_id in grouped_by_course_df.index], rotation=45)
# Adding the student numbers above each bar
for i, (course_id, mean_word_count) in enumerate(grouped_by_course_df.items()):
    ax.text(i, mean_word_count + 5, str(course_number_and_total_student_count_dict.get(course_id, '')), ha='center')

plt.title("Mean Word Counts of Dr. S—'s Responses to Student Discussion Board Posts")
plt.ylabel("Mean Word Count")
plt.xlabel("Semester/Year")
plt.show()


created_at_sorted_df = df.sort_values(by='created_at')

labels_dict = {course['canvas_course_id']: course['semester_year'] for course in grad_course_dictionary}
course_title_dict = {entry['canvas_course_id']: entry['class_title'] for entry in grad_course_dictionary}

color_map = {
    1170080: 'red',
    1174400: 'blue',
    1170638: 'orange',
    1159984: 'green',
    1158588: 'magenta',
    1170054: 'brown',
    1163662: 'yellow',
    1170078: 'black'
}

created_at_sorted_df['color'] = created_at_sorted_df['course_id'].map(color_map)
fig = px.scatter(created_at_sorted_df, x='created_at', y='word_count', color='color') #hover_data=['comment'])
fig.update_traces(
    name='',  # Remove the default legend title
    legendgroup='course_id',
    showlegend=True,
    hovertemplate='%{customdata}<br>%{x}<br>%{y}',
    customdata=[course_title_dict.get(course_id, 'Unknown') for course_id in created_at_sorted_df['course_id']],
)
for trace in fig.data:
    if trace.name:
        trace.name = course_title_dict.get(int(trace.name), 'Unknown')

fig.update_layout(legend_title='Course Titles')

fig.show()

# Create a dictionary to map the 'canvas_course_id' to 'class_title'
course_title_dict = {entry['canvas_course_id']: entry['class_title'] for entry in grad_course_dictionary}

course_ids = created_at_sorted_df['course_id'].unique()

legend_entries = []
for course_id in course_ids:
    class_title = course_title_dict.get(int(course_id), 'Unknown')
    legend_entries.append({'course_id': course_id, 'class_title': class_title})

fig = go.Figure()

for entry in legend_entries:
    data = created_at_sorted_df[created_at_sorted_df['course_id'] == entry['course_id']]
    fig.add_trace(go.Scatter(
        x=data['created_at'],
        y=data['word_count'],
        name=entry['class_title'],
        mode='markers',
        marker=dict(color=px.colors.qualitative.G10[legend_entries.index(entry)]),
        #marker=dict(color=color_map.get(entry['course_id'])),
        opacity=1
    ))

fig.update_layout(
    title_text="Word Counts Scatterplot of Dr. S—'s Responses to Student Discussion Board Posts",
    title_x=0.5,
    width=1200,
    height=500,
    xaxis=dict(title='Created At'),
    yaxis=dict(title='Word Count'),
)

fig.update_layout(legend_title='Course Titles')

fig.show()

# Create a dictionary to map the 'canvas_course_id' to 'class_title'
course_title_dict = {entry['canvas_course_id']: entry['class_title'] for entry in grad_course_dictionary}

course_ids = created_at_sorted_df['course_id'].unique()

legend_entries = []
for course_id in course_ids:
    class_title = course_title_dict.get(int(course_id), 'Unknown')
    legend_entries.append({'course_id': course_id, 'class_title': class_title})

fig = go.Figure()
# Add a scatter trace with jitter
fig.add_trace(go.Scatter(
    x=created_at_sorted_df['created_at'] + np.random.uniform(-0.2, 0.2, len(created_at_sorted_df)),
    y=created_at_sorted_df['word_count'],
    mode='markers',
    marker=dict(
        color=[color_map.get(course_id) for course_id in created_at_sorted_df['course_id']],
        symbol='circle',
        size=6,
        opacity=0.7,
        line=dict(width=0.5)
    ),
    name='Scatter Plot'
))

fig.show()