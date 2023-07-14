from bs4 import BeautifulSoup
import requests

url = r'https://kspicer80.github.io/post_tenure_review_spring_2023/ptrr.html'

response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

main_content_div = soup.find('div', id='main-content')
#print(main_content_div.prettify())

makenzie_start_id = 'working-with-my-greatest-and-most-favorite-student-in-my-entire-career-as-a-teacherscholar-makenzie-hope-munson-22'
makenzie_end_id = 'mathematics-literature-and-philosophy-with-william-d.-mastin-22'

start_h1 = main_content_div.find('h1', id='teaching')
#print(start_h1)
start_h2 = start_h1.find_next('h2', id=makenzie_start_id)
#print(start_h2)
makenzie_end_h2 = main_content_div.find('h2', id=makenzie_end_id)
#print(makenzie_end_h2)

selected_elements = []
current_element = start_h2.find_next_sibling()

while current_element and current_element != makenzie_end_h2:
    selected_elements.append(current_element)
    current_element = current_element.find_next_sibling()

word_count = 0

for element in selected_elements:
    text = element.get_text(strip=True)
    words = text.split()
    word_count += len(words)

print("Total number of words in MaKenzie's section: ", word_count)

william_start_id = 'mathematics-literature-and-philosophy-with-william-d.-mastin-22'
william_end_id = 'concluding-remarks-on-teaching-as-a-whole'

start_h1 = main_content_div.find('h1', id='teaching')
#print(start_h1)
start_h2 = start_h1.find_next('h2', id=william_start_id)
#print(start_h2)
william_end_h2 = main_content_div.find('h2', id=william_end_id)
#print(william_end_h2)

selected_elements = []
current_element = start_h2.find_next_sibling()

while current_element and current_element != william_end_h2:
    selected_elements.append(current_element)
    current_element = current_element.find_next_sibling()

word_count = 0

for element in selected_elements:
    text = element.get_text(strip=True)
    words = text.split()
    word_count += len(words)

print("Total number of words in William's section: ", word_count)
