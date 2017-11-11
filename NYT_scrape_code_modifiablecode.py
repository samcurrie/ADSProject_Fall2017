#Note: when putting this program in your terminal window type "python" "filename.py" '
#Elsewise this will fail'

import time
import requests
import sys
from nytimesarticle import articleAPI
api = articleAPI('Insert your key here') #note you will have to input the key here once you sign up for the API

def fetchlist_singlepage(page):
    allurls = []
    articles = api.search( q = 'Williamsburg change', #enter keyword for body of text here
        fq = { 'source':['The New York Times']}, #specify source publications
        begin_date = 20000101, #this is the begin date - in order to collect all documents - modify based on your last query
        end_date = 20091231, #this is the end date, which should not change until Dec 31 2009 has been hit
        sort='oldest', #this sorts documents by oldest first
        page=page ) #specify begin dates
    docs = articles['response']['docs'] #subscripting by these keys to get the article date and url
    for doc in docs:
        info = {
        'url': (doc['web_url']),
        'date': (doc['pub_date'][0:10])
        }
        allurls.append(info) #append to our list of urls
    return allurls



def fetchlist():    #this function will create a list from the prior function
    allurls = []
    for page in range(10):  #this grabs articles from the first 10 pages working backwords
        time.sleep(1) #pauses the program for 1 second
        print('processing urls')    #to keep track of progress, print statement will appear
        allurls_singlepage = fetchlist_singlepage(page)
        allurls += allurls_singlepage
    return allurls

def fetchurl(url):  #this function accesses the url and extracts the contents
    contents = requests.get(url)
    contenttext = contents.text
    return contenttext

def fetch_processed_article(url):   #this parses the html and returns the text
    from bs4 import BeautifulSoup
    bodytext = ''
    html = fetchurl(url)
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.findAll('p', attrs={'class': 'story-body-text'})
    for paragraph in result:
        bodytext += paragraph.text + '\n'
    return bodytext

def write_processed_article(url, name): #this function writes the text into a txt file from next function
    bodytext = fetch_processed_article(url)
    article = open(name, "w")
    article.write(bodytext.encode('utf-8'))
    article.close()

def filename_for_info(info):    #this function assigns the file name for the previous one
    url_mod = info['url'].replace("/", "_") #'/' replaced with '_'
    url_mod = url_mod.replace(":", "_") #':' replaced with '_'
    return info['date'] + url_mod +".txt"   #all parts of filename assembled


def write_all_articles():   #this final function assembles previous functions together by fetching and writing the articles
    infos_for_process = fetchlist()
    article_urls = []
    article_text = []
    for each_info in infos_for_process:
        print('fetching urls')
        article_urls.append(each_info['url'])
        name = filename_for_info(each_info)
        print('writing articles')
        write_processed_article(each_info['url'], name)

write_all_articles()
