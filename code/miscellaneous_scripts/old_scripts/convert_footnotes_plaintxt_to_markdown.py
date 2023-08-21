import re

def convert_html_to_markdown(text):
    # Convert HTML hyperlinks to markdown links
    text = re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', text)

    # Convert <em> tags to markdown emphasis (italic)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)

    return text

# Read the input plain text file
with open('input.txt', 'r') as file:
    input_text = file.read()

# Convert the HTML and <em> tags to markdown
output_text = convert_html_to_markdown(input_text)

# Write the converted text to the output markdown file
with open('output.md', 'w') as file:
    file.write(output_text)