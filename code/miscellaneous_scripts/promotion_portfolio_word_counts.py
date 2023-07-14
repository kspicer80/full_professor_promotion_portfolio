import requests
from bs4 import BeautifulSoup
import html2text
import PyPDF2


pages_to_check = [
    'https://sites.google.com/stfrancis.edu/choispost-tenurereview/teaching',
    'https://sites.google.com/stfrancis.edu/choispost-tenurereview/scholarship',
    'https://sites.google.com/stfrancis.edu/choispost-tenurereview/service'
    ]

def count_words_in_html(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    word_count = 0
    for p in soup.find_all('p'):
        text = p.get_text()
        words = text.split()
        print(words[0:100])
        word_count += len(words)
    return word_count

word_counts_dict = {}

# Usage
#web_page_url = 'https://sites.google.com/stfrancis.edu/choispost-tenurereview/scholarship'  # Replace with your web page URL
#word_count = count_words_in_html(web_page_url)
#print(f"Total words on in Dr. Choi's Portfolio: {word_count}")

print(f"Total number of words in Dr. Choi's Portfolio: {8822+4058+3335}")

for number, web_page in enumerate(pages_to_check):
    word_count = count_words_in_html(web_page)
    word_counts_dict[number] = word_count

print(word_counts_dict)


def count_words_in_pdf(filename):
    total_words = 0

    with open(filename, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            words = text.split()
            total_words += len(words)

    return total_words

'''
def count_words_in_heading_tags_with_html2text(url_to_parse):
    response = requests.get(url_to_parse)
    soup = BeautifulSoup(response.text, 'html.parser')
    heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section']
    converter = html2text.HTML2Text()

    result = {}  # Dictionary to store the results

    for tag in heading_tags:
        headings = soup.find_all(tag)

        for heading in headings:
            total_word_count = 0  # Initialize word count for each heading
            paragraphs = heading.find_all_next('p')

            for paragraph in paragraphs:
                plain_paragraph = converter.handle(str(paragraph))
                paragraph_word_count = len(plain_paragraph.split())
                total_word_count += paragraph_word_count

            result[tag] = total_word_count  # Store the total word count for the heading tag

    return result

url = r'https://kspicer80.github.io/post_tenure_review_spring_2023/ptrr.html'

# Print the results
#word_counts = count_words_in_heading_tags_with_html2text(url)

#for heading_tag, word_count in word_counts.items():
    #print(f'{heading_tag}: {word_count} words')

def count_words_in_heading_tags_with_html2text_by_specific_id(url_to_parse, target_heading_id):
    response = requests.get(url_to_parse)
    soup = BeautifulSoup(response.text, 'html.parser')
    heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section']
    converter = html2text.HTML2Text()

    result = {}  # Dictionary to store the results

    for tag in heading_tags:
        headings = soup.find_all(tag)

        for heading in headings:
            heading_id = heading.get('id')

            if heading_id == target_heading_id:
                total_word_count = 0  # Initialize word count for the target heading

                # Iterate over the siblings of the heading tag
                for sibling in heading.next_siblings:
                    if sibling.name == 'p' and sibling.get('id') is not None and sibling.get('id').startswith('para_'):
                        plain_paragraph = converter.handle(str(sibling))
                        paragraph_word_count = len(plain_paragraph.split())
                        total_word_count += paragraph_word_count
                    elif sibling.name in heading_tags:
                        break  # Stop processing if a new heading level is encountered

                result[tag] = total_word_count  # Store the total word count for the target heading

    return result

makenzie_heading_id = 'working-with-my-greatest-and-most-favorite-student-in-my-entire-career-as-a-teacherscholar-makenzie-hope-munson-23'

word_counts = count_words_in_heading_tags_with_html2text_by_specific_id(url, makenzie_heading_id)

# Print the result for the target heading
if makenzie_heading_id in word_counts:
    word_count = word_counts[makenzie_heading_id]
    print(f'Total words for Heading ID "{makenzie_heading_id}": {word_count}')
else:
    print(f'Heading ID "{makenzie_heading_id}" not found or no paragraphs with IDs starting with "para_" underneath.')
'''
# Usage example
#count_words_in_heading_tags_with_lxml(url)

# Usage
ee_pdf_file = r'G:\My Drive\full_professor_promotion_portfolio\sample_portfolios\ee_full_professor_portfolio.pdf'
word_count = count_words_in_pdf(ee_pdf_file)
print(f"Total words in the Dr. Evans' Portfolio: {word_count}")

#ks_post_tenure_review_pdf = r"C:\Users\KSpicer\Desktop\ptrr.pdf"
#word_count = count_words_in_pdf(ks_post_tenure_review_pdf)
#print(f"Total words in the Spring 2023 Post-Tenure Review Reflection PDF: {word_count}")

#ks_full_promotion_pdf_file = r'G:\My Drive\full_professor_promotion_portfolio\full_professor_promotion_reflection.pdf'
#word_count = count_words_in_pdf(ks_full_promotion_pdf_file)
#print(f"Total words in the current full promotion PDF: {word_count}")

