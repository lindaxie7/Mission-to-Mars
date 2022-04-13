#!/usr/bin/env python
# coding: utf-8

# In[182]:


# import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up Html parser
html = browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('div.list_text') # look for <div class=list_text>, select_one: return the first matching element

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div',class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)



# find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url =f'https://spaceimages-mars.com/{img_url_rel}'
print(img_url)


# ### Mars Facts

# using pd.read_html to read HTML table as dataframe
df= pd.read_html('https://galaxyfacts-mars.com/')[0]
df

df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace= True)
df

# add the DataFrame to a web application > convert to html
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

html = browser.html
hemi_soup = soup(html, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
hemisphere = hemi_soup.find_all('div', class_='description')

for x in range(len(hemisphere)):
    hemispheres = {}
    browser.find_by_css('img.thumb')[x].click()
    
    # retrieve the data
    title = browser.find_by_css('h2.title').text
    url = browser.links.find_by_text("Sample")['href']
    
    # save data as dictionary
    hemispheres['img_url'] = url
    hemispheres['title'] = title
    
    # append the dictionary data in the hemispheres list
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# end the automated browsing session
browser.quit()




