# import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
        'news_title' : news_title,
        'news_paragraph' : news_paragraph,
        'featured_image' : featured_image(browser),
        'facts' : mars_facts(),
        'last_modified' : dt.datetime.now(),
        'hemispheres': hemisphere_data(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up Html parser
    html = browser.html
    news_soup = soup(html,'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text') 
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div',class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
    except AttributeError:
            return None, None

    return news_title, news_p


def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url =f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():

    try:
        # using pd.read_html to read HTML table as dataframe
        df= pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace= True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

def hemisphere_data(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    hemisphere = hemi_soup.find_all('div', class_='description')

    try:
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
    except:
        return None, None
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

