#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def scrape_info():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News

    nasa_news_url = 'https://mars.nasa.gov/news'
    browser.visit(nasa_news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    news_title = news_soup.find('div', class_="content_title")
    news_p = news_soup.find("div", class_ ="article_teaser_body")
    news_title_text = news_title.text.strip()
    news_p_text = news_p.text.strip()
    print(f"news_title = {news_title_text}")
    print(f"news_p = {news_p_text}")
    #mars_info["news_title"] = news_title_text
    #mars_info["news_p"] = news_p_text
    news = [news_title, news_p]
    # return news

    #JPL Mars Space Images - Featured Image

    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_image_url)
    #Clicking Thru to Needed Page
    browser.click_link_by_partial_text('FULL IMAGE')
    import time
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    #Searching w/i needed page
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    main_img_url = image_soup.find('img', class_='main_image')
    hires_img_url = main_img_url.get('src')
    full_img_url = f"https://www.jpl.nasa.gov{hires_img_url}"
    print(f"featured_image_url = {full_img_url}")
    #mars_info["featured_image_url"] = full_img_url
    # return full_img_url

    #Mars Weather

    twitter_w_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_w_url)
    # Retrieve page with the requests module
    response_weather = requests.get(twitter_w_url)
    soup_weather = BeautifulSoup(response_weather.text, 'lxml')
    soup_weather.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_weather_tweet = soup_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()
    #mars_info["mars_weather"] = mars_weather_tweet
    # return mars_weather_tweet

    #OLD
    #html = browser.html
    #weather_soup = BeautifulSoup(html, "html.parser")
    #mars_weather_tweet1 = weather_soup.find_all("div", class_= "css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t r-bnwqim r-qvutc0")
    #mars_weather_tweet = mars_weather_tweet1.find_all("span", class_= "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
    print(mars_weather_tweet)


    #Mars Facts

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    tables = pd.read_html(facts_url)
    mars_facts_df = (tables[0])                                   
    mars_facts_df.columns = ["Measurements", "Values"]
    #mars_facts_df = mars_facts_df.set_index("Measurements")
    mars_html = mars_facts_df.to_html() #(index = True, header =True)
    print(mars_html)
    #mars_info["mars_facts"] = mars_html
    # return mars_html


    #Mars Hemispheres

    mars_Hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_Hem_url)
    html = browser.html
    Hem_soup = BeautifulSoup(html, "html.parser")
    mars_Hem = []

    results= Hem_soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        Hem_url = hemisphere.find("a")["href"]
        Hem_page = "https://astrogeology.usgs.gov/" + Hem_url    
        browser.visit(Hem_page)
        html = browser.html
        Hem2_soup=BeautifulSoup(html, "html.parser")
        downloads = Hem2_soup.find("div", class_="downloads")
        img_url = downloads.find("a")["href"]
        mars_Hem.append({"title": title, "img_url": img_url})

    print("hemisphere_image_urls =")
    #mars_info["mars_hemisphere"] = mars_Hem
    # return mars_Hem

    mars_info = {
        "news_title": news_title_text,
        "news_p": news_p_text,
        "featured_image_url": full_img_url,
        "mars_weather": mars_weather_tweet,
        "mars_facts": mars_html,
        "mars_hemisphere": mars_Hem

    }


    browser.quit()
    return mars_info

if __name__ == "__main__":
    print(scrape_info())



