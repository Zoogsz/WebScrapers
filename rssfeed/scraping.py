# imports
import requests
from bs4 import BeautifulSoup
import soupsieve
import json

hackernewsURl = "https://news.ycombinator.com/rss"
#scraping function
def hackernews_rss(url) :
    article_list = [] # empty list declaration
    try:
        r = requests.get(url)
        # return print ("The scraping job succeeded:", r.status_code)
        soup = BeautifulSoup(r.content, features='xml')
        
        articles = soup.findAll('item')# parse for 'item' at the beginning of  each feed structure

        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            article = {
                'title' : title,
                'link' : link,
                'published': published
            }
            article_list.append(article)
        # return print(articles)
        return save_function(article_list)   
    except Exception as e:
            print("The scraping job failed. See exception")
            print(e)

def save_function(article_list):
    with open("hackernews.txt","w") as outfile:
        for a in article_list:
            outfile.write(str(a))
            outfile.write("\n")
        outfile.close()

print('Starting scraping')
hackernews_rss(hackernewsURl)
print('Finished scraping')    