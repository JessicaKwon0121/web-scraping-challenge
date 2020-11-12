import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import os
import time

data = {}


def init_browser():
    executable_path = {'executable_path': '/Users/jessicakwon/Desktop/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    mars_news(browser)
    featured_image(browser)
    mars_facts()
    hemispheres(browser)

    browser.quit()
    return data


def mars_news(browser):
    print("mars_news")

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    browser.is_element_present_by_name("email", wait_time=2)

    html = browser.html
    soup = bs(html, "html.parser")

    list_text = soup.find("div", class_="list_text")
    title = list_text.find("div", class_='content_title').get_text()
    paragraph = list_text.find('div', class_="article_teaser_body").get_text()

    data["title"] = title
    data["paragraph"] = paragraph

    print(f"title is: {title}")
    print(f"title is: {paragraph}")

    return


def featured_image(browser):
    print("featured_image")

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)

    full_image = browser.find_by_id("full_image")
    full_image.click()

    browser.is_element_present_by_text("more info", wait_time=2)
    more_info = browser.links.find_by_partial_text("more info")
    more_info.click()

    html = browser.html
    img_soup = bs(html, "html.parser")

    img_url = img_soup.select_one("figure.lede a img").get("src")
    img_link = f"https://www.jpl.nasa.gov{img_url}"

    data["featured_image_url"] = img_link

    return


def mars_facts():
    print("mars_facts")

    df = pd.read_html("http://space-facts.com/mars/")[0]

    df.columns = ["Mars Facts", "Values"]
    data["facts"] = df.to_html(index=False)

    return


def hemispheres(browser):
    print("hemispheres")

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_hemispheres = []

    for i in range(4):

        images = browser.find_by_tag('h3')
        images[i].click()
        time.sleep(5)

        html = browser.html
        soup = bs(html, 'html.parser')

        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2", class_="title").text
        img_url = 'https://astrogeology.usgs.gov' + partial

        dictionary = {"title": img_title, "img_url": img_url}
        mars_hemispheres.append(dictionary)
        browser.back()

    data["hemisphere_image"] = mars_hemispheres

    return
