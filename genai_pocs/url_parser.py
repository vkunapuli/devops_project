import requests
from bs4 import BeautifulSoup

def extract_links_and_sections(url):
   try:
       # Fetch the web page content
       response = requests.get(url)
       response.raise_for_status()  # Raise an error for bad responses

       # Parse the content with BeautifulSoup
       soup = BeautifulSoup(response.content, 'html.parser')
       for tag in soup.findAll(True):
           print(tag.name)

       # Initialize a list to hold a dictionary of URLs and section names
       links_and_sections = []

       for a_tag in soup.find_all('a', href=True):
           href = a_tag['href']
           # Get the section name (anchor text)
           section_name = a_tag.get_text(strip=True)  # Use strip=True to remove extra whitespace
           
           # Append the dictionary with URL and section name, skip mailto or javascript
           if href.startswith('http'):
               links_and_sections.append({'url': href, 'name': section_name})

       return links_and_sections

   except requests.exceptions.RequestException as e:
       print(f"Error fetching URL: {e}")
       return []

# Example usage
web_url = 'https://guide.freddiemac.com/'  # Replace with your desired URL
links_sections = extract_links_and_sections(web_url)
for link in links_sections:
   print(f"Section Name: {link['name']}, URL: {link['url']}")
print('done')
