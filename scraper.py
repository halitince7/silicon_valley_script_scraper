import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin
import time

def get_episode_links(url):
    """Get all episode links from the main page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all episode links
    episode_links = []
    for link in soup.find_all('a', href=True):
        if 'season-' in link['href'] and 'episode-' in link['href']:
            full_url = urljoin(url, link['href'])
            episode_links.append(full_url)
    
    return episode_links

def extract_script(url):
    """Extract script content from an episode page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the script div
    script_div = soup.find('div', class_='full-script')
    if script_div:
        return script_div.get_text(strip=True)
    return None

def get_episode_info(url):
    """Extract season and episode numbers from URL."""
    match = re.search(r'season-(\d+)/episode-(\d+)', url)
    if match:
        season = match.group(1)
        episode = match.group(2)
        return f"s{season}e{episode}"
    return None

def main():
    # Create output directory if it doesn't exist
    if not os.path.exists('scripts'):
        os.makedirs('scripts')
    
    # Main URL
    base_url = 'https://subslikescript.com/series/Silicon_Valley-2575988'
    
    # Get all episode links
    print("Getting episode links...")
    episode_links = get_episode_links(base_url)
    
    # Process each episode
    for url in episode_links:
        print(f"Processing {url}...")
        
        # Get episode info for filename
        episode_id = get_episode_info(url)
        if not episode_id:
            print(f"Could not extract episode info from {url}")
            continue
        
        # Extract script
        script = extract_script(url)
        if not script:
            print(f"Could not extract script from {url}")
            continue
        
        # Save script to file
        filename = f"scripts/{episode_id}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"Saved {filename}")
        
        # Be nice to the server
        time.sleep(1)

if __name__ == "__main__":
    main()
