# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ****************************************************************
# JPL SPACE IMAGES FEATURED IMAGE

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ****************************************************************
# MARS FACTS

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

# ****************************************************************
# SCRAPE HIGH-RESOLITION MARS' HEMISPHERE IMAGES AND TITLES

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')

# full_image_links = img_soup.find_all('a', class_='product-item')
full_image_links = browser.find_by_css('a.product-item img')
# print(full_image_links)

for i in range(len(full_image_links)):
    hemispheres = {}
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css('a.product-item img')[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.links.find_by_text('Sample').first

    # sample_elem.inspect()
    # get the href from sample_elem ---> 'img_url'
    hemispheres["img_url"] = sample_elem["href"]

    # get the h2.title text from this page ---> 'title'
    hemispheres["title"] = browser.find_by_css("h2.title").text
    
    # append the results to hemisphere_image_urls as a dictionary
    hemisphere_image_urls.append(hemispheres)
    # to go back to the main page
    browser.back() 

print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()