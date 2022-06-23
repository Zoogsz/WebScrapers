#tasks.py

# RabbitMQ
# sudo rabbitmq-server
# Celery Worker
# celery worker -A tasks -B -l INFO
# worker - starts worker process
# -A tasks - Stating we want the tasks app
# -B calls for the worker to execute beat schedule
# -l INFO - Ensure we have verbose console logging events (details)

from celery import Celery
import requests # pulling data
from bs4 import BeautifulSoup #XML parsing
import json #exporting to files
from datetime import datetime
from celery.schedules import crontab  # scheduler

app = Celery('tasks') # app name defination
#hackernewsURL = "https://news.ycombinator.com/rss"

#@app.task # registering the task to the app
#def add(x, y): # 
#    return x + y

# Scheduled task execut

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'tasks.hackernews_rss',
        'schedule': crontab(),
    },
}


@app.task
def hackernews_rss() :
    article_list = [] # empty list declaration
    try:
        print("Starting tool")
        r = requests.get("https://news.ycombinator.com/rss")
        # return print ("The scraping job succeeded:", r.status_code)
       # print("requestedRss feed")
        soup = BeautifulSoup(r.content, features='xml')
       #print("pulled feed")
        
        articles = soup.findAll('item')# parse for 'item' at the beginning of  each feed structure
        #print("item parsed")

        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            article = {
                'title' : title,
                'link' : link,
                'published': published,
                'created_at':str(datetime.now()),
                'source': 'HackerNews RSS'
            }
            article_list.append(article)
        # return print(articles)
        return save_function(article_list)   
    except Exception as e:
            print("The scraping job failed. See exception")
            print(e)

@app.task
def save_function(article_list):

    #timestamp and filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    filename = 'articles-{}.json'.format(timestamp)

    #creating article files with timestamp
    with open("hackernews.txt","w") as outfile:
        json.dump(article_list, outfile)
        outfile.close()

print('Starting scraping')
hackernews_rss()
print('Finished scraping')    
 




