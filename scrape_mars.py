import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():

    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Save the browser's html attribute and clean it using BeautifulSoup
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # WRITE YOUR OWN CODE TO DEFINE THIS STRING
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text
     
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Save the browser's html attribute and clean it using BeautifulSoup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    relative_image_url_scraped_from_site = img_soup.find_all('div', class_='floating_text_area')[0].find('a')['href']
    
    # Use the base url to create an absolute url
    featured_image_url = f'https://spaceimages-mars.com/{relative_image_url_scraped_from_site}'
    

    # WHEN USING THE pd.read_html function, WHY DO YOU THINK WE HAD TO GET THE ZERO-th INDEX?
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    

    # WRITE YOUR OWN CODE TO CLEAN THIS DATAFRAME
    df.columns = ['Description', 'Mars', 'Earth']
    df = df.set_index('Description')
    
    # CONVERT TO HTML :)
    # YAY PAND
    mars_facts = df.to_html()
    mars_facts = mars_facts.replace(mars_facts[25:34], 'dataframe; table table-responsive table-striped" style="text-align: left;')

   # Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write a for loop to retrieve the image urls and titles for each hemisphere in the url above.
    html = browser.html
    results = BeautifulSoup(html, 'html.parser')
    
    hemispheres = results.find_all('div', class_='item')

    for hemisphere in hemispheres:
        hemi = {}
        hemi['title']= hemisphere.find('h3').text
        browser.visit(f"{url}{hemisphere.find('a')['href']}")
        hemi_html = browser.html
        hemi_results = BeautifulSoup(hemi_html, 'html.parser')
        hemi['img_url'] = f"{url}{hemi_results.find('img',class_='wide-image')['src']}"
        hemisphere_image_urls.append(hemi)


    # Finally, close the Google Chrome window...
    browser.quit()


    scraped_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts": mars_facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    return scraped_data
