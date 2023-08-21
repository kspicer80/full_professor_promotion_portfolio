import re
from bs4 import BeautifulSoup

def extract_custom_tags(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        custom_tags_list = []
        counter = 0


        for label in soup.find_all('label', class_='margin-toggle sidenote-number'):
            label_for = label.get('for')
            span_tag = label.find_next('span', class_='sidenote')

            if label_for and span_tag:
                footnote_content = ''.join(str(item) for item in span_tag.contents)
                custom_tag_data = {
                    'sidenote_id': label_for,
                    'replaced_with': counter,
                    'footnote_text': footnote_content
                }
                custom_tags_list.append(custom_tag_data)
                counter += 1

        # Save the extracted custom tags in a new file
        #with open(output_file, 'w', encoding='utf-8') as output:
            #output.write(str(soup))

        return custom_tags_list

def replace_custom_tags_with_footnotes(html_file, custom_tags_list):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    for custom_tag_data in custom_tags_list:
        # Create the regex pattern to search for the exact key (custom tag) in the HTML content
        custom_tag_pattern = rf"<label class=\"margin-toggle sidenote-number\" for=\"{custom_tag_data['sidenote_id']}\"></label>"
        # Replace the custom tag with markdown-style footnote
        footnote_format = f"[^{custom_tag_data['replaced_with']}]"
        content = re.sub(custom_tag_pattern, footnote_format, content)

    # Save the modified HTML content back to the file
    with open('converted_html.html', 'w', encoding='utf-8') as output:
        output.write(content)

import re

def replace_custom_tags_with_footnotes_v1(html_file, custom_tags_list):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    for custom_tag_data in custom_tags_list:
        # Create the regex pattern to search for the exact key (custom tag) in the HTML content
        custom_tag_pattern = rf"<label class=\"margin-toggle sidenote-number\" for=\"{custom_tag_data['sidenote_id']}\"></label><input class=\"margin-toggle\" id=\"{custom_tag_data['sidenote_id']}\" type=\"checkbox\"/>"
        # Replace the custom tag and <input> tag with markdown-style footnote
        footnote_format = f"[^{custom_tag_data['replaced_with']}]"
        content = re.sub(custom_tag_pattern, footnote_format, content)
    
    content = re.sub(r"<input[^>]*>", "", content)
    # Save the modified HTML content back to the file
    with open('intermediate.html', 'w', encoding='utf-8') as output:
        output.write(content)

def strip_input_tags(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create the regex pattern to match the input tags with the specified class
    input_tag_pattern = r"<input[^>]*class=\"margin-toggle\"[^>]*>"
    
    # Remove all occurrences of the input tags with the specified class
    content = re.sub(input_tag_pattern, "", content)

    # Save the modified HTML content back to the file
    with open('stripped_input_tags.html', 'w', encoding='utf-8') as output:
        output.write(content)

def strip_sidenote_tags(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create the regex pattern to match the input tags with the specified class
    copilot_sidenote_tag_pattern = r"<span[^>]*class=\"sidenote\"[^>]*>.*?</span>"
    
    # Remove all occurrences of the input tags with the specified class
    content = re.sub(copilot_sidenote_tag_pattern, "", content)

    # Save the modified HTML content back to the file
    with open('stripped_sidenote_tags.html', 'w', encoding='utf-8') as output:
        output.write(content)

def generate_footnotes_output(custom_tags_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for data in custom_tags_list:
            replaced_with = data['replaced_with']
            footnote_text = data['footnote_text']

            file.write(f"[^{replaced_with}]: {footnote_text}\n")

def find_markdown_escaped(input_text):
    # Define the regex pattern to find the footnote references
    pattern = r"\[\^\d+\]"

    def replace_match(match):
        digit = int(match.group()[2:-1])
        return f"[^{digit}]"

    output_text = re.sub(pattern, replace_match, input_text)
    return output_text

html_file_path = 'full_professor_promotion_reflection.html'
converted_file_path = 'converted_html.html'
stripped_input_tags_file_path = 'stripped_input_tags.html'

custom_tags_list = extract_custom_tags(html_file_path)
print(custom_tags_list[0])

generate_footnotes_output(custom_tags_list, 'footnotes_output.txt')

replace_custom_tags_with_footnotes_v1(html_file_path, custom_tags_list)
strip_input_tags(converted_file_path)
strip_sidenote_tags(stripped_input_tags_file_path)
print("Conversion Done!")

