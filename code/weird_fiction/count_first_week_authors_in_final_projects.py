import json
from collections import defaultdict
import docx2txt
import matplotlib.pyplot as plt
import os
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import pprint as pp
import PyPDF2
import seaborn as sns

input_dir = r'C:\Users\KSpicer\Desktop\final_projects\data_folders'

data = []
for subdir, dirs, files in os.walk(input_dir):
    for file in files:
        filepath = os.path.join(subdir, file)
        extension = os.path.splitext(file)[-1].lower()
        if extension == '.txt':
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    data.append((subdir, file, file_content))
            except UnicodeDecodeError:
                print(f"Skipping file {file} due to UnicodeDecodeError")
        elif extension == '.pdf':
            try:
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfFileReader(f)
                    pdf_content = ''
                    for page in range(pdf_reader.getNumPages()):
                        pdf_content += pdf_reader.getPage(page).extractText()
                    data.append((subdir, file, pdf_content))
            except PyPDF2.utils.PdfReadError:
                print(f"Skipping file {file} due to PyPDF2.utils.PdfReadError")
        elif extension == '.docx':
            try:
                docx_content = docx2txt.process(filepath)
                data.append((subdir, file, docx_content))
            except:
                print(f"Skipping file {file} due to an error")

df = pd.DataFrame(data, columns=['Folder', 'Filename', 'Content'])
df.to_json('folder_file_content.json', orient='records')

# Load the extracted content from JSON
with open('folder_file_content.json', 'r') as f:
    extracted_data = json.load(f)

with open(r'G:\My Drive\DHStuff\projects\weird_fiction_from_scratch\author_list\author_list.json') as f:
    aliases_data = json.load(f)

# Define the author_id numbers we're interested in:
desired_id_numbers = [1, 2, 3, 4, 5, 123, 124]

# Create a defaultdict to store the counts
counts = defaultdict(int)

# Iterate through the extracted data
for data in extracted_data:
    content = data['Content']
    folder = data['Folder']
    filename = data['Filename']

    # Iterate through the aliases and check if they exist in the content
    for item in aliases_data:
        id_number = item['id_number']
        if id_number in desired_id_numbers:
            aliases = item['aliases']
            for alias in aliases:
                if alias.lower() in content.lower():
                    counts[(folder, filename, id_number)] += 1

# Create a new dictionary to store the folder, filename, id_number, and alias counts
result = []
for key, value in counts.items():
    folder, filename, id_number = key
    result.append({
        'Folder': folder,
        'Filename': filename,
        'id_number': id_number,
        'Count': value
    })

# PrettyPrint the result or write it to a new JSON file—we'll just prettyprint it here b/c we're going to plot it in a second
pp.pprint(result)

df = pd.DataFrame(result)
print(df.head())

total_counts = df.groupby('id_number')['Count'].sum()
plt.bar(total_counts.index.unique(), total_counts.values)
plt.xlabel('author_id')
plt.ylabel('Total Counts')
plt.title('Total Counts of First-Week Authors Mentioned in Final Projects')
plt.show()
plt.clf()

sns.barplot(x=total_counts.index, y=total_counts.values)
plt.xlabel('author_id')
plt.ylabel('Total Counts')
plt.title('Total Counts of First-Week Authors Mentioned in Final Projects')
plt.show()

