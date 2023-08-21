import re

def extract_sidenotes(text):
    pattern = r'(?<=\[)(.+?)(?=\]\{#(\d+) \.sidenote\})'
    sidenotes = {}
    for match in re.finditer(pattern, text, re.DOTALL):
        value = match.group(1).strip()
        key = match.group(2)
        print(f"Found sidenote {key}: {value}")
        sidenotes[key] = value
    return sidenotes

# Rest of the code remains the same

markdown_file = 'full_professor_promotion_reflection.md'

with open(markdown_file, 'r') as f:
    text = f.read()

markdown_content = re.sub(r'\{target="_blank"\}', '', text)

#print(text)
sidenotes = extract_sidenotes(text)

for key, value in sidenotes.items():
    print(f"Found sidenote {key}: {value}")
