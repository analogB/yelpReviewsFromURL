#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 13:33:41 2018

@author: brad
"""
### IMPORT NON STANDARD LIBRARIES
from bs4 import BeautifulSoup #pip install beautifulsoup4
import requests  #pipenv install requests

#IMPORT STANDARD LIBRARIES
import re 
import time

file_name = 'reviews_file.txt'

#USER INPUT: LIST OF YELP BUSINESS CODENAMES
url_biz_list =[ #ten vienemese restaurants in san jose
    'com-tam-dat-thanh-san-jose',
    'com-tam-thien-huong-san-jose',
    'com-tam-thien-huong-san-jose-2',
    'dalat-restaurant-san-jose',
    'duc-huong-gio-cha-sandwiches-san-jose',
    'huong-lan-sandwich-san-jose-2',
    'nam-vang-restaurant-san-jose',
    'pho-ga-nha-chicken-pho-house-san-jose-2',
    'phu-quy-san-jose-2',
    'vit-dong-que-san-jose'
    ]

url_biz_list =[ #ten vienemese restaurants in san jose
    'com-tam-dat-thanh-san-jose',
    'com-tam-thien-huong-san-jose']


### LOOP OVER EACH BUSINESS
for url_biz in url_biz_list: #[url_biz_list[0]]:
    
    ### ASSEMBLE URL FOR YELP REVIEW BUSINESS
    url_yelp = 'https://www.yelp.com/biz/' #yelp's base biz url
    url_base = url_yelp + url_biz #this should take you to the main page for the business
    
    ### CREATE A NAVIGABLE STRING FOR THE URL'S HTML
    soup_n_pages = BeautifulSoup(requests.get(url_base).text,'lxml')
    
    ### FIND THE NUMBER OF PAGES OF REVIEWS FOR THE BUSINESS
    n_pages_class = "page-of-pages arrange_unit arrange_unit--fill" #this is the css class of the number of review pages
    n_pages_string = soup_n_pages.find_all(class_ = n_pages_class)[0].contents[0] #string that contains number of pages
    n_pages = int(re.search("Page 1 of (\d+)",n_pages_string).group(1)) #number of pages
      
    ### LOOP OVER EACH PAGE
    for page in range(n_pages): #(range(1)) #for each review page
        
        ### INITIATE A BLANK LIST OF REVIEWS FOR PAGE
        reviews=[]
        
        ### BE A POLITE WEB CRAWLER
        time.sleep(1) #wait a second (the routine generally takes longer anyway tho)
        
        ### ASSEMBLE THE PAGE URL
        url_ext = '?start=' + str(page*20) #url extension for review page
        url_reviews = url_base + url_ext #full url
        
        ### CREATE A NAVIGABLE STRING FOR THE URL'S HTML
        soup_reviews = BeautifulSoup(requests.get(url_reviews).text,'lxml') 
        
        ### FIND THE REVIEW AND AUTHOR CONTAINERS AND ASSEMBLE INTO LISTS
        review_table = soup_reviews.find_all(class_ = 'review-content') #reviews
        author_table = soup_reviews.find_all(class_ = 'user-name') #authors
    
        ### LOOP OVER EACH REVIEW CONTAINER
        for i in range(len(review_table)): #for each review container
            
            ### REMOVE PAGE BREAK TAGS
            for linebreak in review_table[i].find_all('br'): #remove line breaks
                linebreak.extract()
            
            ### REMOVE LINK REFERENCES THAT THROW OFF THE SEARCHABLE STRING
            for link in review_table[i].find_all('a'): #remove <a> tag elements
                link.extract() 
                
            ### GET THE REVIEW CONTENTS AND AUTHOR NAME
            review = (' '.join(review_table[i].find('p').contents)).replace(u'\xa0', u' ') #take the review contents
            author = author_table[i].find('a').contents[0] #take the author name
            rating = review_table[i].find('img').parent.attrs['title'][0]
            
            ### APPEND TO REVIEW LIST
            reviews.append([url_biz,author,rating,review]) # 0-business; 1-author; 2-review
    
        ### WRITE REVIEWS TO FILE
        with open(file_name,'a') as file:
            for review in reviews:
                file.write("%s\n" % review)

### CLOSE FILE AT END
file.close()
