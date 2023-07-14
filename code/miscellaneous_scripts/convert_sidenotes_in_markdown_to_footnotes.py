import re
from markdown_it import MarkdownIt

def convert_sidenotes_to_footnotes(markdown_file, output_file):
    with open(markdown_file, 'r') as file:
        markdown_content = file.read()

    footnotes = {}
    md = MarkdownIt()

    # Parse the markdown content
    tokens = md.parse(markdown_content)

    for token in tokens:
        if token.type == "fence" and token.tag == "span" and token.info == "{# .sidenote}":
            sidenote_label = token.content

            # Extract the sidenote ID and letter (if present)
            match = re.match(r'(\d+[a-z]*)', sidenote_label)
            if match:
                sidenote_id = match.group(1)

                # Find the sidenote content
                sidenote_pattern = r'{#' + sidenote_label + r'}(.*?){#/' + sidenote_label + r'}'
                sidenote_match = re.search(sidenote_pattern, markdown_content, re.DOTALL)

                if sidenote_match:
                    sidenote_text = sidenote_match.group(1).strip()

                    # Construct the footnote key
                    footnote_key = f"[^{sidenote_id}]"
                    footnote_value = f"{footnote_key}: {sidenote_text}"
                    footnotes[sidenote_label] = footnote_value

                    # Replace the sidenote with the footnote reference in the markdown content
                    markdown_content = re.sub(sidenote_pattern, footnote_key, markdown_content)

    # Write the converted markdown content to the output file
    with open(output_file, 'w') as file:
        file.write(markdown_content)

    # Append the footnotes at the end of the output file
    with open(output_file, 'a') as file:
        file.write('\n\n')
        for footnote_value in footnotes.values():
            file.write(footnote_value + '\n')


markdown_file_path = r"G:\My Drive\full_professor_promotion_portfolio\full_professor_promotion_reflection_markdown_test.md"
output_file_path = r'G:\My Drive\full_professor_promotion_portfolio\full_professor_promotion_reflection_markdown_to_markdown_test.md'


convert_sidenotes_to_footnotes(markdown_file_path, output_file_path)
