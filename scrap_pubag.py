import requests
import json
import argparse

API_KEY = "jGgEv0rYItqngfgOd9eF9HN5GoCDRxTzB64slFdL"

parser = argparse.ArgumentParser(description='Scraping tool PubAg')
parser.add_argument('--query', type=str, metavar='Q',
                    help="search keywords")
parser.add_argument('--abs_file', type=str, default="abs_dict_pubag.json",metavar='A',
                    help="dictionary of abstracts file")
parser.add_argument('--maxPage', type=int, default=0, metavar='E',
                    help="number of pages max to scrap for a given query")
args = parser.parse_args()

    
# Open json file
abstract_dict_file = args.abs_file
with open(abstract_dict_file) as f:
    abs_dict = json.load(f)

if len(abs_dict)==0:
    abs_dict["titles"] =[]
    abs_dict["abstracts"]=[]
    abs_dict["authors"]=[]
    abs_dict["keywords"]=[]
    abs_dict["sources"]=[]
    abs_dict["dates"]=[]

# Find total pages for query
query_word = args.query
print("Searching results for {}".format(query_word))

query_word_converted = query_word.replace(' ','+')
request = "https://api.nal.usda.gov/pubag/rest/search/?query={}&per_page=100&page={}&api_key={}".format(query_word_converted,1,API_KEY)

response = requests.get(request).json()

totalPages = response["request"]["totalPages"]
print("Total Pages found : {}".format(totalPages))

# Scrap abtracts
maxPages = totalPages if args.maxPage==0 else args.maxPage
nb_abstract = 0

print("Scrap {} pages for {}".format(maxPages,query_word))

for page in range(1,maxPages+1):
    request = "https://api.nal.usda.gov/pubag/rest/search/?query={}&per_page=100&page={}&api_key={}".format(query_word_converted,page,API_KEY)
    response = requests.get(request).json()

    results = response["resultList"]
    len_page = len(results)
    
    for i in range(len_page):
        print('Page {}/{}'.format(page,maxPages), end='\r')
        title = results[i]["title"]

        try: abstract = results[i]["abstract"]
        except: continue

        try: source = results[i]["journal"]
        except: source = "unknown"

        try: authors = results[i]["author"]
        except: authors = "unknown"

        try: keywords = results[i]["subject"]
        except: keywords = "unknown"

        try: date = results[i]["publication_year"]
        except: date = "unknown"
        
        if title not in abs_dict["titles"]:  
            nb_abstract += 1
            abs_dict["titles"].append(title)
            abs_dict["abstracts"].append(abstract)
            abs_dict["authors"].append(authors)
            abs_dict["keywords"].append(keywords)
            abs_dict["sources"].append(source)
            abs_dict["dates"].append(date)


print('Parsed {}'.format(nb_abstract))

with open(abstract_dict_file, 'w+') as f:
    json.dump(abs_dict, f)