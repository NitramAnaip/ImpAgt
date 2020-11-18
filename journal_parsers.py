import os
import json
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bs4 import BeautifulSoup 
import requests
import io
import PyPDF2



# Load driver (for Google Chrome)  
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


def article_source(soup):
    type_publication = soup.find('dt',text='Type of publication')
    publisher = soup.find('dt',text='Publisher')
    document_type = soup.find('dt',text='Document type')

    if publisher != None:
        source = publisher.find_next("span").text
        return source

    elif type_publication != None:
        type_publication = type_publication.find_next("span").text

        if type_publication.lower() == 'journal paper':
            source = soup.find('dt',text='Source').find_next("span").text
            source = source.split('Publisher:')[1].split('Country')[0]
            return source

    elif document_type != None:
        document_type = document_type.find_next("span").text.lower()
        if (document_type == 'working paper') | (document_type == 'report'):
            return 'arxiv'

    return 'unknown'


def sciencedirect_abstract_parser(driver, url, abs_dict, keywords, source):
    """
    ARGS: url is the url of the journal/abstract/article you wnt to get
        abs_dict is the dictionnary containing all our data (abstracts, doi s, authors ...)
    """
    try:
        #DOI
        doi = driver.find_element_by_class_name("doi").text
        start = doi.find("doi.org", 0, -1)+8
        end=doi.find("/", start, -1)
        doi = doi[start:end]
        
        title = driver.find_element_by_class_name("title-text").text
        abstract = driver.find_element_by_class_name("abstract.author").text

        given_names = driver.find_elements_by_class_name("text.given-name")
        surnames = driver.find_elements_by_class_name("text.surname")
        authors_list = []
        for i in range (len(surnames)):
            authors_list.append(given_names[i].text + " " + surnames[i].text)
        
        if title not in abs_dict["titles"]:
            abs_dict["titles"].append(title)
            abs_dict["abstracts"].append(abstract)
            abs_dict["doi"].append(doi)
            abs_dict["authors"].append(authors_list)
            abs_dict["keywords"].append(keywords)
            abs_dict["sources"].append(source)
        print("other abstract added")
    except:
        print("problem with url")


    return 0


def mdpi_abstract_parser(driver, url, abs_dict, keywords, source):
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        #DOI
        doi = driver.find_element_by_class_name("bib-identity").text
        start = doi.find("doi.org", 0, -1) + 8
        end=doi.find("/", start, -1)
        doi = doi[start:end]
        
        abstract = driver.find_element_by_class_name('art-abstract.in-tab.hypothesis_container').text
        title = driver.find_element_by_class_name("title.hypothesis_container").text

        authors = soup.select("div.art-authors.hypothesis_container span.sciprofiles-link a")
        authors_list = []
        for author in authors:
            authors_list.append(author.text)

        if title not in abs_dict["titles"]:
            abs_dict["titles"].append(title)
            abs_dict["abstracts"].append(abstract)
            abs_dict["doi"].append(doi)
            abs_dict["authors"].append(authors_list)
            abs_dict["keywords"].append(keywords)
            abs_dict["sources"].append(source)
    except:
        print("problem with url")

    return 0

# HAL content_provider
def HAL_abstract_parser(driver, url, abs_dict, keywords, source):

    try:
            #DOI
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        doi = soup.select("div.widget.widget-identifiants ul li:contains('DOI')")
        if len(doi)==0: doi = 'unknown'
        else: 
            doi = doi[0].text[6:13]
        
        #print("doi: ", doi)
        try:
            abstract = driver.find_element_by_class_name('abstract-content').text
        except:
            print("No abstract in {}".format(url))
            return 0

        title = driver.find_element_by_class_name("title").text
        #print("title ", title)

        # authors = driver.find_elements_by_class_name("authors")
        authors = soup.select("div.authors span.author a")
        authors_list = []
        for author in authors:
            authors_list.append(author.text)
        # print(authors)   

        #print("authors: ", authors_list)

        if title not in abs_dict["titles"]:
            abs_dict["titles"].append(title)
            abs_dict["abstracts"].append(abstract)
            abs_dict["doi"].append(doi)
            abs_dict["authors"].append(authors_list)
            abs_dict["keywords"].append(keywords)
            abs_dict["sources"].append(source)
    except:
        print("problem with url")

    return 0

# public library of science publisher
def public_lib_science_abstract_parser(driver, url, abs_dict, keywords, source):

    try:
        #DOI
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        doi = soup.find(id='artDoi')
        if len(doi)==0: doi = 'unknown'
        else: 
            doi = doi.text[17:24]
        
        try:
            abstract = soup.select('div.abstract.toc-section p')[0].text
        except:
            print("No abstract in {}".format(url))
            return 0

        title = soup.select("div.title-authors h1")[0].text

        authors = soup.select("div.title-authors ul li a.author-name")
        authors_list = []
        for author in authors:
            authors_list.append(author.text[1:])

        if title not in abs_dict["titles"]:
            abs_dict["titles"].append(title)
            abs_dict["abstracts"].append(abstract)
            abs_dict["doi"].append(doi)
            abs_dict["authors"].append(authors_list)
            abs_dict["keywords"].append(keywords)
            abs_dict["sources"].append(source)
    except:
        print("problem with url")

    return 0

# springer
def nature_abstract_parser(driver, url, abs_dict, keywords, source):

    try:
        #DOI
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        doi = 'unknown'
        
        try:
            abstract = soup.select('div.c-article-section__content p')[0].text
        except:
            print("No abstract in {}".format(url))
            return 0

        title = soup.select("div.c-article-header h1")[0].text

        authors = soup.select("div.c-article-header li.c-author-list__item span a")
        authors_list = []
        for author in authors:
            authors_list.append(author.text)

        if title not in abs_dict["titles"]:
            abs_dict["titles"].append(title)
            abs_dict["abstracts"].append(abstract)
            abs_dict["doi"].append(doi)
            abs_dict["authors"].append(authors_list)
            abs_dict["keywords"].append(keywords)
            abs_dict["sources"].append(source)
    except:
        print("problem with url")

    return 0


def pdf_abstract_parser(driver, url, abs_dict, keywords, source):
    try:
        pdf = requests.get(url)
        with io.BytesIO(pdf.content) as f:
            reader = PyPDF2.PdfFileReader(f)
            print(reader.getDocumentInfo())
    except:
        print("problem with url")



def ieee_abstract_parser(driver, url, abs_dict, keywords, source):
    try:
        #DOI

        doi = 'unknown'
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        try:
            abstract = soup.find('meta',attrs={'property': 'og:description'})['content']

        except:
            print("No abstract in {}".format(url))
            return 0

        title = soup.select("div.document-header-title-container.col h1")[0].text

        authors = soup.select("div.authors-banner-row-middle span.blue-tooltip a")

        authors_list = []
        for author in authors:
            authors_list.append(author.text)

        if title not in abs_dict["titles"]:
            abs_dict["titles"].append(title)
            abs_dict["abstracts"].append(abstract)
            abs_dict["doi"].append(doi)
            abs_dict["authors"].append(authors_list)
            abs_dict["keywords"].append(keywords)
            abs_dict["sources"].append(source)
    except:
        print("problem with url")

    return 0


"""
#BEWARE THIS IS A REINITILISATION OF OUR SAVED DATA. DO NOT USE UNLESS UTTERLY SURE OF WHAT YOU ARE DOING
abstract_dict = {"doi" : [], "titles" : [], "abstracts" : [], "authors" : [], "keywords" : [], "sources" : []}

with open('abs_dict.json', 'w+') as f:
    json.dump(abstract_dict, f)
"""