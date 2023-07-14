from bs4 import BeautifulSoup

with open('full_professor_promotion_reflection_stripped_new_lines.html', 'r', encoding='utf-8') as file:
    html = file.read()
soup = BeautifulSoup(html, 'html.parser')

for p in soup.find_all('blockquote'):
    p.string = p.text.replace('\n', ' ')

with open('full_professor_promotion_reflection_stripped_new_lines.html', 'w') as file:
    file.write(str(soup))