import sys
import re
import html2markdown
from bs4 import BeautifulSoup
import html2text

def convert_sidenotes_to_footnotes(html_file, markdown_file):
    with open(html_file, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    footnotes = {}
    sidenote_labels = soup.find_all('label', {'class': 'margin-toggle', 'for': re.compile('^sn-')})

    for label in sidenote_labels:
        label_id = label.get('for')
        sidenote_id = label_id.replace('sn-', '')

        sidenote = soup.find('span', {'id': sidenote_id, 'class': 'sidenote'})

        if sidenote is not None:
            sidenote_text = sidenote.get_text(strip=True)
            #sidenote_link = sidenote.find('a')
            #if sidenote_link is not None:
                #sidenote_url = sidenote_link['href']
                #sidenote_text += f", available [{sidenote_link.get_text()}]({sidenote_url})"

            footnote_id = len(footnotes) + 1
            footnote_key = f"[^{footnote_id}]"
            footnote_value = f"{footnote_key}: {sidenote_text}"
            footnotes[sidenote_id] = footnote_value

            label.string = footnote_key
            label['for'] = ''
            label['class'] = 'footnote-ref'

            # Replace the sidenote with the footnote reference in the main text
            for element in soup.find_all(text=re.compile(r'\b' + re.escape(sidenote_id) + r'\b')):
                if element.parent.name not in ['label', 'sup']:
                # Check if the element is within a heading tag
                    if element.parent.name.startswith('h'):
                        element.replace_with(re.sub(r'\b' + re.escape(sidenote_id) + r'\b', '', element))
                    else:
                        element.replace_with(re.sub(r'\b' + re.escape(sidenote_id) + r'\b', footnote_key, element))

    markdown_converter = html2text.HTML2Text()
    markdown_content = markdown_converter.handle(str(soup))

    for sidenote_id, footnote_value in footnotes.items():
        markdown_content = markdown_content.replace(f'id="{sidenote_id}" class="sidenote"', 'class="footnote"')

    # Write the converted markdown content to the output file
    with open(markdown_file, 'w') as file:
        file.write(markdown_content)

    # Append the footnotes at the end of the markdown file
    with open(markdown_file, 'a') as file:
        file.write('\n\n')
        for footnote_value in footnotes.values():
            file.write(footnote_value + '\n')

html_file_path = r'G:\My Drive\full_professor_promotion_portfolio\full_professor_promotion_reflection.html'
markdown_file_path = r'G:\My Drive\full_professor_promotion_portfolio\full_professor_promotion_reflection_markdown_test.md'

convert_sidenotes_to_footnotes(html_file_path, markdown_file_path)

'''
# Usage: python convert_html_to_markdown.py input.html output.md
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python convert_html_to_markdown.py input.html output.md')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_sidenotes_to_footnotes(input_file, output_file)
'''
