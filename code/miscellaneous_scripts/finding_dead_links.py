import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime

def setup_logging():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_filename = f'code/miscellaneous_scripts/logs/dead_link_checker_{timestamp}.log'
    logging.basicConfig(    
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename = log_filename,
        filemode='w'
    )

def find_dead_links(url):
    dead_links = []

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch the page: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True)]

    for link in links:
        full_url = urljoin(url, link)
        try:
            link_response = requests.head(full_url)
            link_response.raise_for_status()
            #print(f"Link {full_url} is alive and well!")
        except requests.exceptions.RequestException as e:
            #logging.warning(f"Link {full_url} is dead and gone!")
            dead_links.append(full_url)

    return dead_links

if __name__ == "__main__":
    setup_logging()
    url_to_page_to_search = 'https://kspicer80.github.io/full_professor_promotion_portfolio/full_professor_promotion_reflection.html'
    dead_links = find_dead_links(url_to_page_to_search)
    logging.info("Dead links are:")
    if dead_links is None:
        logging.info("No dead links found!")
    for link in dead_links:
        logging.info(link)


