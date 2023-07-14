import os

def generate_html_links(root_folder):
    html_links = []
    for root, dirs, files in os.walk(root_folder):
        dir_name = os.path.basename(root)  # Get the directory name
        dir_links = []  # List to store the hrefs within the directory

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_folder)
            href = '/' + relative_path.replace('\\', '/')  # Convert Windows path separator to forward slash
            filename = os.path.splitext(file)[0]  # Get the file name without extension
            html_link = f'<li><a href="{href}">{filename}</a></li>'
            dir_links.append(html_link)

        if dir_links:
            dir_structure = f'<li>{dir_name}<ul>' + '\n'.join(dir_links) + '</ul></li>'
            html_links.append(dir_structure)

    return html_links

# Usage example:
root_folder = r"G:\My Drive\full_professor_promotion_portfolio\supporting_materials\1_teaching\past_syllabi"
links = generate_html_links(root_folder)

# Wrap HTML links in <ul> tag
html_output = '<ul>\n' + '\n'.join(links) + '\n</ul>'
print(html_output)
