import json
import gensim
import numpy as np
from utils import preprocess_corpus


from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig, AutoModelWithLMHead, AutoTokenizer



def main():


    parsed_sites = '../pubag_abs_dict.json'

    print("Started Reading JSON file")
    with open(parsed_sites, "r") as read_file:
        abstract_dict = json.load(read_file)
        print("Decoded JSON Data From File")
    
    for i in range (1):
        ARTICLE = abstract_dict["abstracts"][i]
        print(ARTICLE)
        print(len(ARTICLE))

    
    #BART model
    """
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')

    
    inputs = tokenizer([ARTICLE], max_length=2000, return_tensors='pt')
    # Generate Summary
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=5, early_stopping=True)
    print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids])

    """
    #End of bart model
    #Beginning of t5


    model = AutoModelWithLMHead.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")

    # T5 uses a max_length of 512 so we cut the article to 512 tokens.
    inputs = tokenizer.encode("summarize: " + ARTICLE, return_tensors="pt", max_length=512)
    print(len(inputs[0]))
    print(inputs[0])
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)

    return 0



"""

def main():
    
    abstracts = abstract_dict["abstracts"][:200]
    preprocess_abstract = preprocess_corpus(abstracts, tokenize=True)

    return 0

"""
main()