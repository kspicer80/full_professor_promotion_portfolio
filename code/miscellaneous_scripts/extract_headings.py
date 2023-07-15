from bs4 import BeautifulSoup

def extract_headings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_texts = [heading.get_text() for heading in headings]
    return heading_texts

def extract_headings_with_ids(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    heading_ids = []

    for heading in headings:
        heading_id = heading.get('id')
        if heading_id:
            heading_ids.append(heading_id)

    return heading_ids

def extract_anchor_hrefs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')

    hrefs = []  # List to store the href attributes

    for anchor in anchor_tags:
        href = anchor.get('href')
        if href:
            hrefs.append(href)

    return hrefs

# Read the HTML file
with open('full_professor_promotion_reflection.html', 'r') as file:
    html_content = file.read()

# Extract the headings
headings = extract_headings(html_content)

# Print the extracted headings
for heading in headings:
    print(heading)

ids = extract_headings_with_ids(html_content)

print(ids)

'''
hrefs = extract_anchor_hrefs(html_content)
print("\nAnchor HREFs:")
for href in hrefs:
    print(href)
'''
