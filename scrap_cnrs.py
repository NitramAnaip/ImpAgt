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
from journal_parsers import article_source
from bs4 import BeautifulSoup 
import requests

# Load driver (for Google Chrome)  
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.maximize_window()

url = "https://bib.cnrs.fr/#"
ID = "18CHIMFR3417"
mdp = "MSSLPT"
ressource_type = "article"
keywords = "computer vision farm"
date_from = 2018
date_to = 2020
# source = "ieee"
#american chemical society
# elsevier b.v., elsevier ltd, elsevier(science direct)
# HAL
# mdpi publishing, mpdi ag, mpdi
# public library of science


abstract_dict_file = "abs_dict.json"
with open(abstract_dict_file) as f:
    abs_dict = json.load(f)

print("len of the dict: ", len(abs_dict["titles"]))
print(abs_dict["titles"][-5:])


driver.get(url)

# Authentification
connexion = driver.find_element_by_class_name("login-button.btn.btn-link").click()
via_code = driver.find_element_by_class_name("inist-button.btn.btn-primary.btn-block").click()

# Put a wait time because the window hasn't popped up yet
driver.implicitly_wait(5)
login = driver.find_element_by_class_name('username.form-control')
login.send_keys(ID)
password = driver.find_element_by_class_name('password.form-control')
password.send_keys(mdp)
connect = driver.find_element_by_class_name('fetch-button.api.btn.btn-primary.btn-block').click()
driver.implicitly_wait(10)


# Select if you want to search for books or articles
if ressource_type=="article":  
    article = driver.find_element_by_class_name('nav-item.nav-article.active').click()
    search = driver.find_element_by_class_name('form-control')
elif ressource_type=="book":
    book = driver.find_element_by_class_name('nav-item.nav-publication').click()
    search = driver.find_element_by_class_name('form-control')
    
# Search for ressources using keywords
search.send_keys(keywords)
search.send_keys(Keys.ENTER)

# this is just to ensure that the page is loaded 
driver.implicitly_wait(20)

#Here we will apply a few filters*******************

date_start = driver.find_element_by_class_name('from')
date_start.clear()
date_start.send_keys(date_from)

apply_filter = driver.find_element_by_class_name('fetch-button.title.clearFacet.btn.btn-primary')
driver.execute_script("arguments[0].click();", apply_filter)
driver.implicitly_wait(5)

xpath_publishers = "/html/body/div[1]/div[1]/div/div/div/span/div/div[1]/div/div[2]/div/span/div[6]/div[1]/button[2]/span[1]"
xpath_languages = "/html/body/div[1]/div[1]/div/div/div/span/div/div[1]/div/div[2]/div/span/div[4]/div[1]/button[2]/span[1]"
xpath_content_provider = "/html/body/div[1]/div[1]/div/div/div/span/div/div[1]/div/div[2]/div/span/div[7]/div[1]/button[2]/span[1]"

# button = driver.find_element_by_xpath(xpath_publishers)
# driver.execute_script("arguments[0].click();", button) #extending the language list
# driver.implicitly_wait(5)
    

# Number of links extracted
n_articles = 0

# Set current page
current_page = 1
links = []
n_page_max = 100


while True and current_page<n_page_max:
    # Take to driver directly to the search-results path
    search_result = driver.find_element_by_class_name('search-result')
    try:
        record_list = driver.find_element_by_class_name("record_list")
    except NoSuchElementException:
        print('No result found...')
        # break

    # It renders the JS code and stores all of the information in static HTML code
    notice_opener = driver.find_elements_by_class_name('notice-opener.btn.btn-link')

    for notice in notice_opener:
        driver.execute_script("arguments[0].click();", notice)

    articles = driver.find_elements_by_class_name('record.record-article')
    notice = driver.find_element_by_class_name('dl.notice-list')
    dl_item = driver.find_elements_by_class_name("span.dl-item")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
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
                n_articles += 1

                abs_dict["titles"].append(title[3:])
                abs_dict["abstracts"].append(abstract)
                abs_dict["doi"].append(doi)
                abs_dict["authors"].append(authors_list)
                abs_dict["keywords"].append(keywords)
                abs_dict["sources"].append(source)
        
    print(' {} abstracts since beginning of request'.format(n_articles))
    with open(abstract_dict_file, 'w+') as f:
        json.dump(abs_dict, f)
    # Next page
    pagination = driver.find_element_by_class_name("pagination")
    next_page = driver.find_element_by_class_name("next").click()
    current_page+=1

print('Number of abstracts extracted : {}'.format(n_articles))

with open(abstract_dict_file, 'w+') as f:
    json.dump(abs_dict, f)

driver.quit()
