# Import bibs
import os
import json
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from journal_parsers import sciencedirect_abstract_parser, mdpi_abstract_parser,HAL_abstract_parser,public_lib_science_abstract_parser,pdf_abstract_parser,nature_abstract_parser,ieee_abstract_parser
from utils_scraping import article_source,search_ressource,select_date,article_source,authentificate

from bs4 import BeautifulSoup 
import requests

import argparse

parser = argparse.ArgumentParser(description='RecVis A3 training script')
parser.add_argument('--date_from', type=int, default=2015, metavar='S',
                    help="start date to search articles")
parser.add_argument('--date_to', type=int, default=2021, metavar='E',
                    help="end date")
parser.add_argument('--types', type=str, default='article', metavar='A',
                    help="end date")
parser.add_argument('--keyword', type=str, default='machine learning agriculture', metavar='K',
                    help="end date")
parser.add_argument('--mdp', type=str, default='MSSLPT', metavar='M',
                    help="for login")
parser.add_argument('--ID', type=str, default='18CHIMFR3417', metavar='I',
                    help="for login")
parser.add_argument('--abs_dict', type=str, default='abs_dict_all.json', metavar='A',
                    help="root file for the abstracts dictionary")                
args = parser.parse_args()


# Load driver (for Google Chrome)  
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.maximize_window()

url = "https://bib.cnrs.fr/#"

abstract_dict_file = args.abs_dict
with open(abstract_dict_file) as f:
    abs_dict = json.load(f)

print("len of the dict: ", len(abs_dict["titles"]))
print(abs_dict["titles"][-5:])


driver.get(url)

authentificate(driver,args.ID,args.mdp)
driver.implicitly_wait(10)

search_ressource(driver,args.types,args.keyword)
driver.implicitly_wait(20)

select_date(driver,args.date_from,args.date_to)
driver.implicitly_wait(5)


# # Extract HTMLs page

# Set current page
current_page = 1
n_page_max = 15

soup_list = []

for page in range(n_page_max):
    # Take to driver directly to the search-results path
    search_result = driver.find_element_by_class_name('search-result')
    driver.implicitly_wait(20)
    try:
        record_list = driver.find_element_by_class_name("record_list")
    except NoSuchElementException:
        print('No result found at page {}...'.format(page+1))
        break

    # It renders the JS code and stores all of the information in static HTML code
    notice_opener = driver.find_elements_by_class_name('notice-opener.btn.btn-link')

    for notice in notice_opener:
        driver.execute_script("arguments[0].click();", notice)


    articles = driver.find_elements_by_class_name('div.notice')

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    soup_list.append(soup)

    # # Next page
    pagination = driver.find_element_by_class_name("pagination")
    next_page = driver.find_element_by_class_name("next").click()
    driver.implicitly_wait(20)

print("Parsed {} pages".format(page+1))
driver.quit()


# # Parse the abstracts

# Number of links extracted
n_articles = 0

# Extract infos from HTMLs
for soup in soup_list:
    n_articles_page = 0
    articles = soup.find_all('div', {'class' : 'record record-article'})

    for article in articles:  

        soup = article
        try:
            authors_list=[]
            authors = soup.find('dt',text='Author').find_next("dd").find_all('a')
            for author in authors:
                authors_list.append(author.text)
        except:
            authors_list = 'unkown'
        
        try:
            abstract = soup.find('dt',text='Abstract').find_next("span").text
        except:
            continue

        try:
            doi = soup.find('dt',text='DOI').find_next("span").text[:8]
        except:
            doi = 'unknown'

        source = article_source(soup)

        try:
            title = soup.find('h4',{'class':'title'}).find('a').text.split('[')[0][2:]
        except:
            title = 'unknown'

        if source != 'unknown':
            if title not in abs_dict["titles"]:
                n_articles_page += 1
                abs_dict["titles"].append(title)
                abs_dict["abstracts"].append(abstract)
                abs_dict["doi"].append(doi)
                abs_dict["authors"].append(authors_list)
                abs_dict["keywords"].append(args.keyword)
                abs_dict["sources"].append(source)
    
    print(' {} abstracts parsed on this page'.format(n_articles_page))

    n_articles += n_articles_page

print('Number of abstracts extracted : {}'.format(n_articles))

with open(abstract_dict_file, 'w+') as f:
    json.dump(abs_dict, f)
