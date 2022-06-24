#tasks.py

# RabbitMQ
# sudo rabbitmq-server
# Celery Worker
# celery worker -A tasks -B -l INFO
# worker - starts worker process
# -A tasks - Stating we want the tasks app
# -B calls for the worker to execute beat schedule
# -l INFO - Ensure we have verbose console logging events (details)

# tasks
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import app, shared_task

# job model
from .models import News

# scraping
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import lxml

# logging
from celery.utils.log import get_task_logger

#app = Celery('tasks') # app name defination
#hackernewsURL = "https://news.ycombinator.com/rss"

#@app.task # registering the task to the app
#def add(x, y): # 
#    return x + y

# Scheduled task execut

#app.conf.timezone = 'UTC'

#app.conf.beat_schedule = {
#   executes every 1 minute
 #    'scraping-task-one-min': {
#       'task': 'tasks.hackernews_rss',
#       'schedule': crontab(),
#   },
#}


@shared_task
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
            published_wrong = a.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')

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

@shared_task
def save_function(article_list):

    #timestamp and filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    filename = 'articles-{}.json'.format(timestamp)

    #creating article files with timestamp
    with open("hackernews.txt","w") as outfile:
        json.dump(article_list, outfile)
        outfile.close()


@shared_task(serializer='json')
def save_function(article_list):
    print('starting')
    new_count = 0

    for article in article_list:
        try:
            News.objects.create(
                title = article['title'],
                link = article['link'],
                published = article['published'],
                source = article['source']
            )
            new_count += 1
        except Exception as e:
            print('failed at latest_article is none')
            print(e)
            break
    return print('finished')
    
print('Starting scraping')
hackernews_rss()
print('Finished scraping')    
 




