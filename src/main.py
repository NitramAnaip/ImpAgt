import json
import gensim
import numpy as np
#from utils import preprocess_corpus


from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig, AutoModelWithLMHead, AutoTokenizer, pipeline



def main():


    parsed_sites = '../pubag_abs_dict.json'

    print("Started Reading JSON file")
    with open(parsed_sites, "r") as read_file:
        abstract_dict = json.load(read_file)
        print("Decoded JSON Data From File")
    ARTICLE = ""
    for i in range (1):
        print(len(abstract_dict["abstracts"][i]))
        print(abstract_dict["abstracts"][i])
        ARTICLE += abstract_dict["abstracts"][i]
    #print(ARTICLE)
    



    #BART model
    #1st attempt
    max_len = 400
    """
    summarizer = pipeline("summarization")
    print(summarizer(ARTICLE, max_length=max_len,   min_length=30))


    # use t5 in tf
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")
    print(summarizer(ARTICLE, max_length=max_len,   min_length=30))
    

    print("********* \nPegasus: \n")
    summarizer = pipeline("summarization", model="google/pegasus-arxiv", tokenizer="t5-base")
    print(summarizer(ARTICLE, max_length=max_len,   min_length=30))
    """


    #End of bart model
    #Beginning of t5

    """
    model = AutoModelWithLMHead.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")

    # T5 uses a max_length of 512 so we cut the article to 512 tokens.
    inputs = tokenizer.encode("summarize: " + ARTICLE, return_tensors="pt", max_length=512)
    print(len(inputs[0]))
    #print(inputs[0])
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    print(outputs[0])
    outputs = tokenizer.convert_ids_to_tokens(outputs[0])
    print(outputs)
    """
    return 0



"""

def main():
    
    abstracts = abstract_dict["abstracts"][:200]
    preprocess_abstract = preprocess_corpus(abstracts, tokenize=True)

    return 0

"""
main()