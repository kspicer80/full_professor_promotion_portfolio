from bs4 import BeautifulSoup
from collections import defaultdict

html_file = "full_professor_promotion_reflection.html"

with open(html_file, encoding='utf-8') as file:
    html_data = file.read()
    
# Parse the HTML content
soup = BeautifulSoup(html_data, 'html.parser')

# Find all <span> tags with the class "sidenote"
sidenote_tags = soup.find_all('span', class_='sidenote')

# Extract and print the unique ID numbers from sidenote tags
id_numbers = []
for tag in sidenote_tags:
    if 'id' in tag.attrs:
        id_numbers.append(int(tag['id']))
        
sorted_id_numbers = sorted(id_numbers)
print("All ID numbers from sidenote tags:", sorted_id_numbers)

id_frequency = defaultdict(int)
for num in id_numbers:
    id_frequency[num] += 1

# Find and print duplicate ID numbers
duplicate_id_numbers = [num for num, freq in id_frequency.items() if freq > 1]

if duplicate_id_numbers:
    print("Duplicate ID numbers:", duplicate_id_numbers)
else:
    print("No duplicate ID numbers found.")