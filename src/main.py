import json
import gensim
import numpy as np
#from utils import preprocess_corpus


from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig, AutoModelWithLMHead, AutoTokenizer, pipeline, PegasusTokenizerFast



def main():


    parsed_sites = '../pubag_abs_dict.json'

    print("Started Reading JSON file")
    with open(parsed_sites, "r") as read_file:
        abstract_dict = json.load(read_file)
        print("Decoded JSON Data From File")
    
    for i in range (3):
        ARTICLE = abstract_dict["abstracts"][i]
        print(ARTICLE)
        print(len(ARTICLE))

    
    #BART model
    #1st attempt


    summarizer = pipeline("summarization")
    print(summarizer(ARTICLE, max_length=1000,   min_length=30))

    """
    2nd attempt at BART
    # the results are far less satisfying than those with t5 or with the pipeline method above. There's probably a mistake in the way I'm using it


    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')


    
    inputs = tokenizer([ARTICLE], max_length=2000, return_tensors='pt')
    print(inputs['input_ids'])
    print(len(inputs['input_ids'][0]))
    # Generate Summary
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=5, early_stopping=True)
    print(summary_ids)
    print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids[0]])
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