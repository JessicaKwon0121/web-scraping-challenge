from splinter import Browser
from bs4 import BeautifulSoup as bs
import os
import time

def init_browser():
    executable_path = {'executable_path': '/Downloads/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    browser.is_element_present_by_name("email", wait_time=2)
    html = browser.html
    soup = bs(html, "html.parser")

    title = soup.find("div", class_="content_title").get_text()
    paragraph = soup.find("div", class_="article_teaser_body").get_text()

    return

def featured_image():
    browser = init_browser()
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(2)
    full_image = browser.find_by_id("full_image")
    full_image.click()

    browser.is_element_present_by_text("more info", wait_time=2)
    more_info = browser.links.find_by_partial_text("more info")
    more_info.click()

    html = browser.html
    img_soup = bs(html, "html.parser")

    hemispheres = img_soup.find_all("img", class_="thumb")

    for hemisphere in hemispheres:
        print(hemisphere["src"])
 
    return