#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


#Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}


# In[3]:


browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)


# In[5]:


# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[6]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[7]:


slide_elem.find('div', class_='content_title')


# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[10]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[13]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[14]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[15]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[16]:


df.to_html()


# # D1 Scrape High Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# In[17]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[18]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# HTML object
html = browser.html

# Parse HTML with Beautiful Soup
title_soup = soup(html, 'html.parser')

# Retrieve all elements
items = title_soup.find_all('div', class_='item')

for item in items:
    hemispheres = {}
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    # Retrieve title
    title = item.find('h3').text
    
    # Go to next webpage
    browser.click_link_by_partial_text(title)
    image_page = browser.html
    imgs_soup = soup(image_page, 'html.parser')
    
    # Retrieve link
    link = imgs_soup.find('div', class_='downloads').find('li').a['href']
    
    img_url = url + link
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    
    hemisphere_image_urls.append(hemispheres)
    
    browser.click_link_by_partial_text('Back')


# In[19]:


# 4. Print the list that holds the dictionary of each image url and title.
for item in hemisphere_image_urls:
    print(item)


# In[20]:


# 5. Quit the browser
browser.quit()


# In[ ]:




