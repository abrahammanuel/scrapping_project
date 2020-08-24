import re
import argparse
import logging
import requests
import pandas as pd
import bs4
import lxml.html as html

from common import config

HEADERS = {
    'User-Agent':  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

logging.basicConfig(level=logging.INFO)

logger = logging.Logger(__name__)

def get_section_links(): 
    #return  a list of links to the sections page
    list_sections = []
    url_base =config()["blog_site"][BLOG_SITE]["url"]
    query_sections = config(
    )["blog_site"][BLOG_SITE]['queries_home']['homepage_articles']
    logging.info("beginnin scrapper for: "+url_base)

    try:
        response = requests.get(url_base, headers=HEADERS)
        if response.status_code ==200: 
            response_utf = response.content.decode('utf-8')
            res_parsed=html.fromstring(response_utf)

            list_sections += res_parsed.xpath(query_sections)
        else: 
            raise ValueError(f'Error: {response.status_code}')
    except Exception as e:
        print("Error in request", e )


    print(list_sections)
    return list_sections

def get_article_links(links_section):
    # return a list a links of each article from section page
    logging.info("starting scrapping getting articles links")

    query_link = config()[
        'blog_site'][blog_site]['queries_home']['section_articles']

    links_articles=[]
    for i, link in enumerate(links_section): 
        logging.info("scraping link: "+link)
        try:
            response = requests.get(link, headers=HEADERS)
            if response.status_code == 200: 
                response_utf = response.content.decode('utf-8')
                res_parsed = html.fromstring(response_utf)
                res_query=res_parsed.xpath(query_link)
                links_articles+=res_query
                # print(res_query)

            else: 
                raise ValueError(f'Error: {response.status_code}')
        except Exception as e:
            blogging.error(e)
            
        
    logging.info(len(links_articles))
    return links_articles
    
def get_article_data(links_article): 
    #get return a list of dictionary with the data of  article of each link of each section
    logging.info("starting scrappy of articles")
    query_article = config()[
        'blog_site'][BLOG_SITE]['queries_article']

    articles_list = []
    
    for link in links_article:
        article_dict = {}
        try:
            response = requests.get(link, headers=HEADERS)
            if response.status_code==200:
                response_utf = response.content.decode("utf-8")
                res_parsed = html.fromstring(response_utf)
            else:
                raise Exception(f'Error: {response.status_code} ')
        except Exception as e:
            logging.error(e)
            
        
        for query, value in query_article.items(): 
            try:
                temp = res_parsed.xpath(value)
                article_dict[query]="".join(temp)
                if query== 'date': print("date: ", temp)
            except Exception as e:
                logging.error(f'Error {e}')

        if article_dict and not article_dict['body']: 
            logging.warning("no body in this article")
            continue

        articles_list.append(article_dict)

    return articles_list
def main():
    links_section = get_section_links()
    links_article = get_article_links(links_section)
    articles_data = get_article_data(links_article)
    df = pd.DataFrame.from_dict(articles_data)
    print(df)

    #save as csv withou index
    df.to_csv("preliminar.csv", index=False)
    # for i, k in articles_data: 
    #     print(i, k)
    

if __name__ == "__main__": 
    blog_site_choice = list(config()["blog_site"].keys())

    #use parser to be able to pass arguments in terminal
    parser = argparse.ArgumentParser()
    parser.add_argument('blog_site',
        help="the blog you want to scrapp",
        type=str, choices=blog_site_choice)
    args = parser.parse_args()

    BLOG_SITE = args.blog_site  # get the arguments passed in terminal
    main()

