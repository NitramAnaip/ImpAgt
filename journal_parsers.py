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




# Load driver (for Google Chrome)  
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

def springer_abstract_parser(driver, url, abs_dict, keywords, source):
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
        #DOI

        doi = driver.find_element_by_class_name("bib-identity").text#get_attribute("href")
        start = doi.find("doi.org", 0, -1) + 8
        end=doi.find("/", start, -1)
        doi = doi[start:end]
        
        #print("doi: ", doi)
        abstract = driver.find_element_by_class_name('art-abstract.in-tab.hypothesis_container').text
        title = driver.find_element_by_class_name("title.hypothesis_container").text
        #print("title ", title)
        authors = driver.find_elements_by_class_name("sciprofiles-link__link")
        
        authors_list = []
        for author in authors:
            authors_list.append(author.text)

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




"""
#BEWARE THIS IS A REINITILISATION OF OUR SAVED DATA. DO NOT USE UNLESS UTTERLY SURE OF WHAT YOU ARE DOING
abstract_dict = {"doi" : [], "titles" : [], "abstracts" : [], "authors" : [], "keywords" : [], "sources" : []}

with open('abs_dict.json', 'w+') as f:
    json.dump(abstract_dict, f)
"""